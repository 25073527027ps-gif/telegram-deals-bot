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

        r = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(r.text, "html.parser")

        title = "Hot Deal Product"
        image = None

        # AMAZON
        if "amazon" in url:

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

        # FLIPKART
        elif "flipkart" in url:

            title_tag = soup.find(
                "meta",
                attrs={"property": "og:title"}
            )

            if title_tag:
                title = title_tag.get("content")

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
