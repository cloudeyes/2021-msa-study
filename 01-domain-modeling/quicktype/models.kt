// To parse the JSON, install kotlin's serialization plugin and do:
//
// val json      = Json(JsonConfiguration.Stable)
// val integer   = json.parse(Integer.serializer(), jsonString)
// val batch     = json.parse(Batch.serializer(), jsonString)
// val order     = json.parse(Order.serializer(), jsonString)
// val orderLine = json.parse(OrderLine.serializer(), jsonString)

package quicktype

import kotlinx.serialization.*
import kotlinx.serialization.json.*
import kotlinx.serialization.descriptors.*
import kotlinx.serialization.encoding.*

@Serializable
data class Batch (
    val reference: String,
    val sku: String,
    val qty: Long,
    val allocations: List<OrderLine>
)

@Serializable
data class OrderLine (
    val id: String,
    val sku: String,
    val qty: Long
)

@Serializable
data class Order (
    val reference: String,
    val orderLines: List<OrderLine>
)
