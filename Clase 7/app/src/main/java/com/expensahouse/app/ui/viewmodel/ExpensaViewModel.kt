package com.expensahouse.app.ui.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import androidx.room.withTransaction
import com.expensahouse.app.ExpensaApp
import com.expensahouse.app.data.remote.AndroidSyncPayload
import com.expensahouse.app.data.remote.ExpensaApiClient
import com.expensahouse.app.domain.model.*
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import retrofit2.HttpException
import java.io.IOException

sealed class ExpensaEvent {
    data class AddStock(val name: String, val brand: String, val category: String) : ExpensaEvent()
    data class UpdateStock(val item: StockItem) : ExpensaEvent()
    data class DeleteStock(val item: StockItem) : ExpensaEvent()
    data class OpenUnit(val item: StockItem) : ExpensaEvent()
    data class ConsumeUnit(val item: StockItem) : ExpensaEvent()
    data class ToggleShopping(val id: String) : ExpensaEvent()
    data class UpdateShoppingQuantity(val id: String, val quantity: Int) : ExpensaEvent()
    data class AddShoppingItem(val name: String, val brand: String, val category: String) : ExpensaEvent()
    data class MoveToStock(val item: ShoppingItem) : ExpensaEvent()
    data class DeleteShoppingItem(val id: String) : ExpensaEvent()
    data class AddOffer(val offer: Offer) : ExpensaEvent()
    data class SetBudget(val amount: Double) : ExpensaEvent()
    data class AddExpense(val amount: Double, val category: String) : ExpensaEvent()
    object RefreshData : ExpensaEvent()
    object ResetData : ExpensaEvent()
}

class ExpensaViewModel(application: Application) : AndroidViewModel(application) {

    private val database = (application as ExpensaApp).database
    private val dao = database.dao
    private val api = ExpensaApiClient.service
    private val _syncMessages = MutableSharedFlow<String>(replay = 1, extraBufferCapacity = 1)
    val syncMessages = _syncMessages.asSharedFlow()

    // Estado persistente desde Room
    val stock = dao.getAllStock().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    val shopping = dao.getAllShopping().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    val savedOffers = dao.getAllOffers().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    val userPrefs = dao.getUserPrefs().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), UserPrefs())
    val expenses = dao.getAllExpenses().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    init {
        viewModelScope.launch {
            initializeSynchronization()
        }
    }

    fun onEvent(event: ExpensaEvent) {
        viewModelScope.launch {
            when (event) {
                is ExpensaEvent.AddStock -> {
                    val item = StockItem(name = event.name, brand = event.brand, category = event.category, stockQuantity = 1)
                    dao.insertStock(item)
                    syncWithShopping(item)
                }
                is ExpensaEvent.UpdateStock -> {
                    dao.updateStock(event.item)
                    syncWithShopping(event.item)
                }
                is ExpensaEvent.DeleteStock -> {
                    dao.deleteStock(event.item)
                    dao.deleteShoppingByName(event.item.name)
                }
                is ExpensaEvent.OpenUnit -> {
                    if (event.item.stockQuantity > 0) {
                        val updated = event.item.copy(
                            stockQuantity = event.item.stockQuantity - 1,
                            inUseCount = event.item.inUseCount + 1
                        )
                        dao.updateStock(updated)
                        syncWithShopping(updated)
                    }
                }
                is ExpensaEvent.ConsumeUnit -> {
                    if (event.item.inUseCount > 0) {
                        dao.updateStock(event.item.copy(inUseCount = event.item.inUseCount - 1))
                    }
                }
                is ExpensaEvent.ToggleShopping -> {
                    val item = shopping.value.find { it.id == event.id }
                    item?.let { dao.updateShopping(it.copy(checked = !it.checked)) }
                }
                is ExpensaEvent.UpdateShoppingQuantity -> {
                    val item = shopping.value.find { it.id == event.id }
                    item?.let { dao.updateShopping(it.copy(quantity = event.quantity)) }
                }
                is ExpensaEvent.AddShoppingItem -> {
                    dao.insertShopping(ShoppingItem(
                        name = event.name,
                        brand = event.brand,
                        category = event.category,
                        detail = "Agregado manual"
                    ))
                }
                is ExpensaEvent.MoveToStock -> {
                    val existing = stock.value.find { it.name.equals(event.item.name, true) && it.brand.equals(event.item.brand, true) }
                    if (existing != null) {
                        dao.updateStock(existing.copy(stockQuantity = existing.stockQuantity + event.item.quantity))
                    } else {
                        dao.insertStock(StockItem(
                            name = event.item.name,
                            brand = event.item.brand,
                            category = event.item.category,
                            stockQuantity = event.item.quantity
                        ))
                    }
                    dao.deleteShoppingById(event.item.id)
                }
                is ExpensaEvent.DeleteShoppingItem -> {
                    dao.deleteShoppingById(event.id)
                }
                is ExpensaEvent.AddOffer -> {
                    dao.insertOffer(event.offer)
                }
                is ExpensaEvent.SetBudget -> {
                    val current = userPrefs.value ?: UserPrefs()
                    dao.saveUserPrefs(current.copy(monthlyBudget = event.amount))
                }
                is ExpensaEvent.AddExpense -> {
                    val current = userPrefs.value ?: UserPrefs()
                    dao.saveUserPrefs(current.copy(totalSpent = current.totalSpent + event.amount))
                    dao.insertExpense(Expense(category = event.category, amount = event.amount))
                }
                is ExpensaEvent.RefreshData -> {
                    stock.value.forEach { syncWithShopping(it) }
                }
                is ExpensaEvent.ResetData -> {
                    dao.clearStock()
                    dao.clearShopping()
                    dao.clearOffers()
                    dao.clearExpenses()
                    dao.saveUserPrefs(UserPrefs())
                }
            }
            synchronizeWithWeb(showSuccess = event is ExpensaEvent.RefreshData)
        }
    }

    private suspend fun initializeSynchronization() {
        try {
            if (isLocalDatabaseEmpty()) {
                val remote = api.getSyncSnapshot().data
                if (isLocalDatabaseEmpty()) {
                    database.withTransaction {
                        dao.clearStock()
                        dao.clearShopping()
                        dao.clearOffers()
                        dao.clearExpenses()
                        dao.insertStockItems(remote.stock)
                        dao.insertShoppingItems(remote.shopping)
                        dao.insertOffers(remote.offers)
                        dao.insertExpenses(remote.expenses)
                        dao.saveUserPrefs(remote.userPrefs)
                    }
                    _syncMessages.emit("Datos iniciales descargados desde la web.")
                } else {
                    synchronizeWithWeb()
                }
            } else {
                synchronizeWithWeb()
            }
        } catch (error: IOException) {
            _syncMessages.emit("No se pudo conectar con la web. Los datos siguen guardados en este teléfono.")
        } catch (error: HttpException) {
            _syncMessages.emit("La API respondió HTTP ${error.code()}. Los datos siguen guardados en este teléfono.")
        }
    }

    private suspend fun isLocalDatabaseEmpty(): Boolean =
        dao.getStockSnapshot().isEmpty() &&
            dao.getShoppingSnapshot().isEmpty() &&
            dao.getOffersSnapshot().isEmpty() &&
            dao.getExpensesSnapshot().isEmpty() &&
            dao.getUserPrefsSnapshot() == null

    private suspend fun synchronizeWithWeb(showSuccess: Boolean = false) {
        try {
            val response = api.syncSnapshot(
                AndroidSyncPayload(
                    stock = dao.getStockSnapshot(),
                    shopping = dao.getShoppingSnapshot(),
                    expenses = dao.getExpensesSnapshot(),
                    userPrefs = dao.getUserPrefsSnapshot() ?: UserPrefs(),
                    offers = dao.getOffersSnapshot()
                )
            )
            if (showSuccess) {
                _syncMessages.emit(response.message ?: "Sincronización completada.")
            }
        } catch (error: IOException) {
            _syncMessages.emit("No se pudo conectar con la web. Los datos siguen guardados en este teléfono.")
        } catch (error: HttpException) {
            _syncMessages.emit("La API respondió HTTP ${error.code()}. Los datos siguen guardados en este teléfono.")
        }
    }

    private suspend fun syncWithShopping(item: StockItem) {
        if (item.stockQuantity <= 1) {
            if (shopping.value.none { it.name.equals(item.name, true) }) {
                dao.insertShopping(ShoppingItem(
                    name = item.name,
                    brand = item.brand,
                    category = item.category,
                    detail = "Reposición automática",
                ))
            }
        } else {
            dao.deleteShoppingByName(item.name)
        }
    }
}
