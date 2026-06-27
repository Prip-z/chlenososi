import asyncio
import httpx
import json
import io
from typing import Optional

BASE_URL = "http://localhost:8000/api/v1"

INPUT_DATA = {
  "scenario": {
    "name": "Кубок Енисея — цифровой штурман аэролодки",
    "area": "Красноярское вдхр., Дивногорск (КрасГЭС) → залив Бирюса (ТИМ)",
  },
  "map": {
    "edges": [
      {"from": "Дивногорск", "to": "Полынья", "km": 8, "surface": "water"},
      {"from": "Полынья", "to": "Узел-М", "km": 15, "surface": "ice"},
      {"from": "Дивногорск", "to": "Лёд-1", "km": 11, "surface": "ice"},
      {"from": "Лёд-1", "to": "Узел-М", "km": 13, "surface": "ice"},
      {"from": "Дивногорск", "to": "Камни", "km": 6, "surface": "rocks"},
      {"from": "Камни", "to": "Узел-М", "km": 11, "surface": "ice"},
      {"from": "Дивногорск", "to": "Болото", "km": 7, "surface": "marsh"},
      {"from": "Болото", "to": "Узел-М", "km": 12, "surface": "ice"},
      {"from": "Узел-М", "to": "Шуга", "km": 9, "surface": "slush"},
      {"from": "Шуга", "to": "Бирюса", "km": 6, "surface": "shallow"},
      {"from": "Узел-М", "to": "Чисто", "km": 13, "surface": "ice"},
      {"from": "Чисто", "to": "Бирюса", "km": 9, "surface": "ice"}
    ]
  }
}


NODE_COORDINATES = {
    "Дивногорск": {"lat": 55.9594, "lon": 92.3951},
    "Полынья": {"lat": 55.9750, "lon": 92.4200},
    "Узел-М": {"lat": 56.0100, "lon": 92.5000},
    "Лёд-1": {"lat": 55.9800, "lon": 92.4500},
    "Камни": {"lat": 55.9400, "lon": 92.4100},
    "Болото": {"lat": 55.9300, "lon": 92.4300},
    "Шуга": {"lat": 56.0300, "lon": 92.5500},
    "Чисто": {"lat": 56.0400, "lon": 92.5200},
    "Бирюса": {"lat": 56.0600, "lon": 92.6000}
}

def log_error(step_name: str, response: httpx.Response, payload: Optional[dict]):
    print(f"\n🛑 [ОШИБКА РАНТАЙМА] На этапе: {step_name}")
    print(f"📡 URL запроса: {response.url}")
    if payload:
        print(f"📦 Payload (данные): {json.dumps(payload, ensure_ascii=False)}")
    print("-" * 60)
    print(f"🔢 Статус ответа: {response.status_code}")
    print("📝 Ответ сервера:")
    try:
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except Exception:
        print(response.text)
    print("=" * 60 + "\n")

async def test_upload():
    async with httpx.AsyncClient(timeout=15.0) as client:
        print("1. Создаем карту в БД (отправка формы с файлом)...")
        
        # Готовим текстовые поля формы
        form_data = {
            "name": INPUT_DATA["scenario"]["name"],
            "pmtiles_url": "http://map_storage:9000/forestmaps/yenisei_cup.pmtiles",
            "description": INPUT_DATA["scenario"]["area"]
        }
        
        fake_file = io.BytesIO(b"PMTiles fake binary data content for testing")
        files = {"file": ("yenisei_cup.pmtiles", fake_file, "application/octet-stream")}
        
        try:
            map_res = await client.post(f"{BASE_URL}/maps", data=form_data, files=files)
        except Exception as e:
            print(f"💥 Ошибка подключения к бэкенду: {e}")
            return

        if map_res.status_code not in [200, 201]:
            log_error("POST /api/v1/maps", map_res, form_data)
            return
            
        map_id = map_res.json()["id"]
        print(f"✅ Карта успешно создана! ID карты = {map_id}")

        print("\n2.Создаем вершины (Nodes) через lat/lon...")
        
        node_name_to_id = {}
        
        for node_name, coords in NODE_COORDINATES.items():
            node_payload = {
                "map_id": int(map_id),
                "lat": float(coords["lat"]),
                "lon": float(coords["lon"]),
                "is_walkable": True,
                "terrain_type": "ice" if "Лёд" in node_name or node_name == "Чисто" else "dirt_trail"
            }
            
            res = await client.post(f"{BASE_URL}/nodes", json=node_payload)
            if res.status_code not in [200, 201]:
                log_error(f"POST /api/v1/nodes для '{node_name}'", res, node_payload)
                return
                
            created_node = res.json()
            node_name_to_id[node_name] = created_node["id"]
            print(f"  ✅ Вершина '{node_name}' создана в базе под ID = {created_node['id']}")


        print("\n3. Загружаем ребра используя целочисленные ID...")
        
        for edge in INPUT_DATA["map"]["edges"]:
            source_name = edge["from"]
            target_name = edge["to"]
            
            source_id = node_name_to_id[source_name]
            target_id = node_name_to_id[target_name]
            
            edge_payload = {
                "map_id": int(map_id),
                "source_id": int(source_id),
                "target_id": int(target_id),
                "weight": float(edge["km"])
            }
            
            res = await client.post(f"{BASE_URL}/edges", json=edge_payload)
            if res.status_code not in [200, 201]:
                log_error(f"POST /api/v1/edges ({source_name} -> {target_name})", res, edge_payload)
                return
            print(f"  ✅ Ребро {source_name} (ID: {source_id}) -> {target_name} (ID: {target_id}) загружено.")

        print("\n Все данные успешно отправлены без ошибок!")
        print("4. Тестируем GET запрос на получение вершин...")
        get_res = await client.get(f"{BASE_URL}/nodes")
        
        if get_res.status_code == 200:
            print(f"Роут отдал статус 200. Вернулось нод из базы: {len(get_res.json())}")
        else:
            try:
                data = get_res.json() 
            except:
                data = {"raw_text": get_res.text}

            log_error("GET /api/v1/nodes", get_res, payload=data)

if __name__ == "__main__":
    asyncio.run(test_upload())