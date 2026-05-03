from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import (
    UnitOfInformation,
    PERCENTAGE,
    UnitOfTime,
)

from .const import DOMAIN

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="fw",
        translation_key="fw_version",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="uptime",
        translation_key="uptime",
        icon="mdi:clock-outline",
    ),
    SensorEntityDescription(
        key="iccid",
        translation_key="iccid",
        icon="mdi:sim",
    ),
    SensorEntityDescription(
        key="imsi",
        translation_key="imsi",
        icon="mdi:sim",
    ),
    SensorEntityDescription(
        key="apn",
        translation_key="apn",
        icon="mdi:access-point-network",
    ),
    SensorEntityDescription(
        key="lte_mode",
        translation_key="lte_mode",
        icon="mdi:signal-cellular-3",
    ),

    SensorEntityDescription(
        key="rssi",
        translation_key="rssi",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement="dBm",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="rsrq",
        translation_key="rsrq",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement="dB",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="rsrp",
        translation_key="rsrp",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement="dBm",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="signal_level",
        translation_key="signal_level",
        icon="mdi:signal",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="operator_name",
        translation_key="operator_name",
        icon="mdi:account-network",
    ),
    SensorEntityDescription(
        key="ip",
        translation_key="public_ip",
        icon="mdi:earth",
    ),
    SensorEntityDescription(
        key="download_usage",
        translation_key="download_usage",
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.MEGABYTES,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="upload_usage",
        translation_key="upload_usage",
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.MEGABYTES,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="total_usage",
        translation_key="total_usage",
        device_class=SensorDeviceClass.DATA_SIZE,
        native_unit_of_measurement=UnitOfInformation.MEGABYTES,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="memory",
        translation_key="memory",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:memory",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="cpu",
        translation_key="cpu",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:cpu-64-bit",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="latency_avg_ms",
        translation_key="latency",
        native_unit_of_measurement="ms",
        icon="mdi:speedometer",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="clients",
        translation_key="clients",
        icon="mdi:devices",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="next_update",
        translation_key="next_update",
        icon="mdi:update",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up UMR-Ultra sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for description in SENSOR_TYPES:
        entities.append(UmrUltraSensor(coordinator, entry, description))

    async_add_entities(entities)

class UmrUltraSensor(CoordinatorEntity, SensorEntity):
    """Representation of a UMR-Ultra Sensor."""
    
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, description: SensorEntityDescription):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        # Device info to link all sensors to one device
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
            "manufacturer": "Ubiquiti",
            "model": "UMR-Ultra",
            "sw_version": coordinator.data.get("fw", "Unknown"),
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
            
        if self.entity_description.key == "next_update":
            from homeassistant.util.dt import utcnow
            from datetime import timedelta
            from .const import CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
            interval = self.entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
            return utcnow() + timedelta(seconds=interval)
            
        val = self.coordinator.data.get(self.entity_description.key)
        
        if val is None:
            return None
            
        if self.entity_description.key == "uptime":
            days, remainder = divmod(int(val), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, _ = divmod(remainder, 60)
            parts = []
            if days > 0:
                parts.append(f"{days} Tag{'e' if days > 1 else ''}")
            if hours > 0 or days > 0:
                parts.append(f"{hours} Std.")
            parts.append(f"{minutes} Min.")
            return ", ".join(parts)
            
        # Convert bytes to MB for usage stats
        if self.entity_description.key in ("download_usage", "upload_usage", "total_usage"):
            return round(val / (1024 * 1024), 2)
                
        return val
