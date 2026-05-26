# EXPAND AMAZON SHORT LINK
try:
    if "amzn.in" in url:
        expanded = requests.get(
            url,
            allow_redirects=True,
            headers=headers,
            timeout=10
        )
        url = expanded.url
except:
    pass
    def get_product_details(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 10; Mobile) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Mobile Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:

        # AMAZON SHORT LINK FIX
        if "amzn.in" in url:

            expanded = requests.get(
                url,
                headers=headers,
                allow_redirects=True,
                timeout=10
            )

            url = expanded.url

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(response.text, "html.parser")

        title = "Hot Deal Product"
        image = None

        # TITLE
        title_tag = soup.find(
            "meta",
            attrs={"property": "og:title"}
        )

        if title_tag:
            title = title_tag.get("content")

        # IMAGE
        image_tag = soup.find(
            "meta",
            attrs={"property": "og:image"}
        )

        if image_tag:
            image = image_tag.get("content")

        return title[:120], image

    except Exception as e:

        print(e)

        return "Hot Deal Product", None
