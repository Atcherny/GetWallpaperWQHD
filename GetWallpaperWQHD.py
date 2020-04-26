import shutil
import requests
import bs4

headurl = "https://www.ultrawidewallpaper.com"
page = "/wallpapers?page=1"
save_path = 'C:\\Users\\Alex\\Pictures\\ultrawidewallpaper.com\\'
resolution = "3440x1440"
while True:
    html = requests.get(headurl + page).text
    soup_page = bs4.BeautifulSoup(html, 'html.parser')
    for p in soup_page.find_all("a"):
        pic_page = p.get("href")
        if p.find("img", {"class": "gallery_wallpaper"}) is not None:
            html_paper = requests.get(headurl + pic_page).text
            soup_paper = bs4.BeautifulSoup(html_paper, 'html.parser')
            res = soup_paper.find("div", {"id": "resolution"})
            if res is not None and res.contents[2].replace("\n", "") == resolution:
                img_ref = soup_paper.find("img", {"id": "show_wallpaper"})
                wallpaper = img_ref.get("src")
                name = img_ref.get("alt").replace(" Ultrawide Wallpaper", "").replace("?", "").replace("/", " ")
                print(name + " " + wallpaper)
                r = requests.get(wallpaper, stream=True)
                r.raise_for_status()
                r.raw.decode_content = True  # support Content-Encoding e.g., gzip
                with open(save_path + name + ".jpg", 'wb') as file:
                    shutil.copyfileobj(r.raw, file)
    page = soup_page.find("a", {"class": "next_page"})
    if page == None:
        break
    page = page.get("href")
    assert isinstance(page, object)
    print(headurl + page)
