# 🌐 geoip-builder

[![Release](https://img.shields.io/github/v/release/kirilllavrov/geoip-builder?label=latest)](https://github.com/kirilllavrov/geoip-builder/releases)
[![jsDelivr](https://data.jsdelivr.com/v1/package/gh/kirilllavrov/geoip-builder/badge)](https://www.jsdelivr.com/package/gh/kirilllavrov/geoip-builder)

Автоматическая сборка `geoip.dat` для Xray/V2Ray с акцентом на РФ/БЕЛ сети.

---

## 📦 Категории в geoip.dat

| Категория | Описание | Источники |
|-----------|----------|-----------|
| **`ru`** | IP-адреса России и Беларуси | GeoLite2, DB-IP, ipinfo, countrydb + кастомные списки |
| **`private`** | RFC1918 приватные сети | Локальные диапазоны (10.0.0.0/8, 192.168.0.0/16 и др.) |

> ⚠️ Из категории `ru` **исключаются** IP из списков антифильтров, CDN и трекеров.

---

## 🚀 Использование

### 1. Подключение geoip.dat

Добавьте URL в конфигурацию вашего прокси-клиента:

| Источник | URL |
|----------|-----|
| **GitHub (прямой)** | `https://raw.githubusercontent.com/kirilllavrov/geoip-builder/release/geoip.dat` |
| **jsDelivr CDN** | `https://cdn.jsdelivr.net/gh/kirilllavrov/geoip-builder@release/geoip.dat` |

### 2. Настройка маршрутизации (Xray/V2Ray)

```json
{
  "routing": {
    "rules": [
      {
        "type": "field",
        "ip": ["geoip:ru", "geoip:private"],
        "outboundTag": "direct"
      }
    ]
  }
}
```

## 🧩 Совместимость

| Клиент | Поддержка | Пример правила |
|--------|-----------|---------------|
| **Xray / v2fly-core** | ✅ | `geoip:ru`, `geoip:private` |
| **Mihomo (Clash Meta)** | ✅ | `.mrs` rulesets |
| **sing-box** | ✅ | `.srs` rulesets |
| **Hysteria / Trojan** | ✅ | через Xray-ядро |

---

## 🙏 Благодарности

Проект использует данные и инструменты:

| Ресурс | Назначение | Лицензия |
|--------|------------|----------|
| [v2fly/geoip](https://github.com/v2fly/geoip) | Инструмент сборки | MIT |
| [hydraponique/roscomvpn-geoip](https://github.com/hydraponique/roscomvpn-geoip) | Исходная конфигурация | MIT |

