package com.expensahouse.app.data.remote

import com.expensahouse.app.BuildConfig
import com.expensahouse.app.domain.model.Expense
import com.expensahouse.app.domain.model.Offer
import com.expensahouse.app.domain.model.ShoppingItem
import com.expensahouse.app.domain.model.StockItem
import com.expensahouse.app.domain.model.UserPrefs
import com.google.gson.annotations.SerializedName
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

data class AndroidSyncPayload(
    val stock: List<StockItem>,
    val shopping: List<ShoppingItem>,
    val expenses: List<Expense>,
    @SerializedName("user_prefs") val userPrefs: UserPrefs,
    val offers: List<Offer>
)

data class SyncSnapshot(
    val stock: List<StockItem> = emptyList(),
    val shopping: List<ShoppingItem> = emptyList(),
    val expenses: List<Expense> = emptyList(),
    @SerializedName("user_prefs") val userPrefs: UserPrefs = UserPrefs(),
    val offers: List<Offer> = emptyList()
)

data class SyncResponse(
    val status: String,
    val data: SyncSnapshot,
    val message: String? = null
)

interface ExpensaApi {
    @GET("api/sync")
    suspend fun getSyncSnapshot(): SyncResponse

    @POST("api/sync")
    suspend fun syncSnapshot(@Body payload: AndroidSyncPayload): SyncResponse
}

object ExpensaApiClient {
    val service: ExpensaApi by lazy {
        Retrofit.Builder()
            .baseUrl(BuildConfig.API_BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ExpensaApi::class.java)
    }
}
