# Автоматическая сборка geoip.dat

Этот репозиторий автоматически генерирует бинарный файл `geoip.dat` для использования в прокси-клиентах (например, Xray, V2Ray) с целью маршрутизации трафика.

## Особенности

*   **Объединение источников:** Собирает IP-адреса из различных источников, включая MaxMind GeoLite2, DB-IP, списки от `Re:filter`, `Antifilter`, `ipinfo`, `countrydb`.
*   **Акцент на РФ/БЕЛ:** Основное внимание уделено агрегации и фильтрации IP-адресов, связанных с Россией (RU) и Беларусью (BY).
*   **Настройка категорий:** Использует категории `ru` и `private`.
*   **Фильтрация:** Применяет списки исключений (`CUSTOM-LIST-DEL.txt`) для удаления нежелательных IP-адресов (например, рекламы, трекеров) из целевых списков (RU/BY).
*   **Удаление `0.0.0.0/8`:** Исключает диапазон `0.0.0.0/8` из категории `private`.
*   **Автоматизация:** Сборка запускается автоматически раз в 3 дня или при пуше в ветку `main`.

## Результаты

*   **Файл `geoip.dat`:** Собранный файл находится в ветке `release` и доступен для скачивания через [GitHub Releases](https://github.com/kirilllavrov/geoip-builder/releases) и [jsDelivr CDN](https://cdn.jsdelivr.net/gh/kirilllavrov/geoip-builder@release/geoip.dat).
*   **Ветки:**
    *   `main`: Основной код и конфигурация для сборки.
    *   `release`: Содержит последние собранные `.dat` файлы.
    *   `test-release`: Содержит артефакты сборки из других веток (например, при тестировании изменений).

## Использование

1.  Добавьте URL к `geoip.dat` в настройки вашего прокси-клиента (например, Xray, V2Ray).
    *   **Пример для Xray/V2Ray (GitHub):**
        `https://raw.githubusercontent.com/kirilllavrov/geoip-builder/release/geoip.dat`
    *   **Пример для Xray/V2Ray (jsDelivr CDN):**
        `https://cdn.jsdelivr.net/gh/kirilllavrov/geoip-builder@release/geoip.dat`
2.  В конфигурации маршрутизации (`routing.rules`) используйте категории `geoip:ru` и `geoip:private`.

    **Пример правила маршрутизации:**
    ```json
    {
      "routing": {
        "rules": [
          {
            "type": "field",
            "ip": [
              "geoip:ru",
              "geoip:private"
            ],
            "outboundTag": "direct"
          }
        ]
      }
    }
    ```

## Благодарности

Этот проект использует и вдохновлён следующими ресурсами и людьми:

*   **[v2fly/geoip](https://github.com/v2fly/geoip):** Инструмент для сборки geoip-баз.
*   **[hydraponique/roscomvpn-geoip](https://github.com/hydraponique/roscomvpn-geoip):** Оригинальная конфигурация (`config.json`) и скрипт фильтрации (`ipset_ops.py`), использованные в качестве основы.
*   **[Re:filter](https://github.com/1andrevich/Re-filter-lists):** Списки IP-адресов.
*   **[Antifilter](https://antifilter.download/):** Списки IP-адресов.
*   **[ipinfo.io](https://ipinfo.io/)** и **[countrydb](https://github.com/hydraponique/countrydb)**: Источники данных о географии IP-адресов.
*   **[DB-IP](https://db-ip.com/)**: Источник данных о географии IP-адресов.
*   **[MaxMind GeoLite2](https://dev.maxmind.com/geoip/geolite2/)**: Источник данных о географии IP-адресов.
*   **[PentiumB/CDN-RuleSet](https://github.com/PentiumB/CDN-RuleSet)** и **[mansourjabin/cdn-ip-database](https://github.com/mansourjabin/cdn-ip-database)**: Списки IP-адресов CDN.

