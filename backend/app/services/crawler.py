import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
from collections import defaultdict

tool_url = "https://www2.e-show.tw/edit_makerthon/index.php?option=productm&lang=cht&task=showlist2&id=8"
equipment_url = "https://www2.e-show.tw/edit_makerthon/index.php?option=productm&lang=cht&task=showlist2&id=6"

user_agent = UserAgent()

def get_equipment_data():
    req = requests.get(equipment_url, headers={ 'user-agent': user_agent.random }, timeout=5)
    soup = BeautifulSoup(req.text, 'lxml')

    merged = defaultdict(lambda: {"正取": [], "備取": []})

    for tab in soup.select('div.tab-content'):
        rows = tab.select('tbody tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 6:
                continue
            category = cols[1].get_text(strip=True)
            admitted = [li.get_text(strip=True) for li in cols[4].find_all('li')]
            waiting = [li.get_text(strip=True) for li in cols[5].find_all('li')]

            merged[category]["正取"].extend(admitted)
            merged[category]["備取"].extend(waiting)

    # 移除重複 + 格式化輸出
    result = []
    for category, data in merged.items():
        Mainly = "、".join(sorted(set(data["正取"])))
        standby = "、".join(sorted(set(data["備取"])))
        result.append({
            "類別": category,
            "正取": Mainly,
            "備取": standby
        })

    return result

def get_tool_data():
    req = requests.get(tool_url, headers={'user-agent': user_agent.random}, timeout=5)
    soup = BeautifulSoup(req.text, 'lxml')
    rows = soup.select('div.table-responsive tbody tr')
    team_list = []

    for row in rows:
        cols = row.find_all('td')
        if len(cols) != 2:
            continue
        team_info = cols[1].get_text(strip=True)
        match = re.match(r"(.+)\s+\((\d+)\)", team_info)
        if match:
            name, code = match.groups()
            team_list.append(f"{name.strip()}（{code.strip()}）")

    return "、".join(team_list)

async def crawl():
    return {
        "equipment_data": get_equipment_data(),
        "tool_data": get_tool_data()
    }
