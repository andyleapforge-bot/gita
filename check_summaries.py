import json

with open('assets/json/shlok_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Show shloks from chapter 3
print("Chapter 3 shloks:")
count = 0
for shlok in data[1:]:
    if shlok.get('__1') == 3:
        summary = shlok.get('__8', '')[:70]
        has_hi = '__8_hi' in shlok
        print(f"Shlok {shlok.get('__3')}: {summary}... [HI: {has_hi}]")
        count += 1
        if count >= 10:
            break
