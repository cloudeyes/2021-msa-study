// To parse the JSON, install kotlin's serialization plugin and do:
//
// val json      = Json(JsonConfiguration.Stable)
// val sku       = json.parse(Sku.serializer(), jsonString)
// val integer   = json.parse(Integer.serializer(), jsonString)
// val batch     = json.parse(Batch.serializer(), jsonString)
// val order     = json.parse(Order.serializer(), jsonString)
// val orderLine = json.parse(OrderLine.serializer(), jsonString)

package quicktype

import kotlinx.serialization.*
import kotlinx.serialization.json.*
import kotlinx.serialization.internal.*

@Serializable
data class Batch (
    val allocations: List<OrderLine>,
    val qty: Long,
    val reference: String,

    /**
     * TypeScript-JSON Schema for quicktype code generation.
     */
    val sku: String
)

@Serializable
data class OrderLine (
    val id: String,
    val qty: Long,

    /**
     * TypeScript-JSON Schema for quicktype code generation.
     */
    val sku: String
)

@Serializable
data class Order (
    val orderLines: List<OrderLine>? = null,
    val reference: String
)
