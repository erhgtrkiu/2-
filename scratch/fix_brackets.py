import sys

app_path = r'C:\Users\m3615\samosbor_game\app.js'

with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read()

s = c.find("let script = document.createElement('script');")
e = c.find('function showInterstitialAd()')

if s != -1 and e != -1:
    new_sdk = '''let script = document.createElement('script');
    script.src = "https://yandex.ru/games/sdk/v2";
    script.onload = () => {
        if (typeof YaGames !== 'undefined') {
            YaGames.init()
            .then(initializedSdk => {
                clearTimeout(sdkTimeout);
                ysdk = initializedSdk;
                console.log("Yandex Games SDK successfully initialized.");
                if (ysdk.features && ysdk.features.LoadingProgress) {
                    ysdk.features.LoadingProgress.ready();
                }
                completeInitialization("SDK ГОТОВ");
            })
            .catch(err => {
                clearTimeout(sdkTimeout);
                console.error("Yandex Games SDK init failed:", err);
                completeInitialization("РЕЖИМ: ДЕМО");
            });
        } else {
            clearTimeout(sdkTimeout);
            console.warn("YaGames global object is undefined. Running in Demo Mode.");
            completeInitialization("РЕЖИМ: ДЕМО");
        }
    };
    script.onerror = () => {
        clearTimeout(sdkTimeout);
        console.error("Yandex Games SDK load failed");
        completeInitialization("РЕЖИМ: ОФФЛАЙН");
    };
    document.head.appendChild(script);
}

'''
    c = c[:s] + new_sdk + c[e:]
    
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Fixed SDK brackets.")
else:
    print("Could not find SDK block")
