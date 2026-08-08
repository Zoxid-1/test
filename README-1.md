# Zippy Taxi — ariza holati backend

Bu kichik backend admin Telegram kanalda ✅ Tastiqlash / ❌ Rad etish tugmasini bosganda
holatni saqlaydi va saytga ("Arizalarim" bo'limiga) qaytaradi.

## 1-qadam: Upstash Redis (bepul)

1. https://upstash.com ga kiring, ro'yxatdan o'ting.
2. "Create Database" → nom bering (masalan `zippy-status`) → Region: istalgan.
3. Database ochilgach, "REST API" bo'limidan ikkita qiymatni oling:
   - `UPSTASH_REDIS_REST_URL`
   - `UPSTASH_REDIS_REST_TOKEN`

## 2-qadam: Vercel'ga joylash

1. https://vercel.com ga kiring (GitHub bilan).
2. Bu `zippy-status-backend` papkasini GitHub'ga yuklang (yangi repo yarating), so'ng Vercel'da
   "Add New Project" → repo'ni tanlang → Deploy.
3. Deploy bo'lgach, loyihaning "Settings → Environment Variables" bo'limiga o'ting va qo'shing:
   - `UPSTASH_REDIS_REST_URL` = (1-qadamdan)
   - `UPSTASH_REDIS_REST_TOKEN` = (1-qadamdan)
   - `BOT_TOKEN` = `8826972597:AAEI6rwGx963dmHn5WB27gPvY2jniHXFY3M`
4. O'zgaruvchilarni qo'shgach, "Deployments" bo'limidan qayta deploy qiling (Redeploy),
   chunki environment variable'lar faqat yangi deploy'da ishga tushadi.
5. Sizga shunday manzil beriladi: `https://sizning-loyiha.vercel.app`

## 3-qadam: Telegram webhook'ni ulash

Brauzerda (yoki curl bilan) shu manzilni oching — faqat bir marta:

```
https://api.telegram.org/bot8826972597:AAEI6rwGx963dmHn5WB27gPvY2jniHXFY3M/setWebhook?url=https://sizning-loyiha.vercel.app/api/webhook
```

`{"ok":true,"result":true,...}` javobi kelsa — tayyor, bot endi tugma bosilganda
avtomatik shu backend'ga xabar beradi.

## 4-qadam: Saytga ulash

`drayver-qoshish.html` faylida quyidagi qatorni toping:

```js
const STATUS_API_URL = "";
```

va shunday qiling:

```js
const STATUS_API_URL = "https://sizning-loyiha.vercel.app/api/status?ids=";
```

Shundan keyin "Arizalarim" bo'limidagi "🔄 Holatni yangilash" tugmasi ishlay boshlaydi —
admin ✅ yoki ❌ bosgan arizalar holati saytda ham yangilanadi.

## Eslatma

- Admin tugma bosgach, Telegram'dagi xabarning o'ziga ham "✅ TASDIQLANDI" yoki
  "❌ RAD ETILDI" deb yozib qo'yiladi (xabar tahrirlanadi) — shunday qilib kanaldagilar
  ham allaqachon ko'rib chiqilgan arizani darhol bilib oladi.
- Bu yechim pullik emas — Upstash va Vercel'ning bepul tarifi bu hajmdagi ish uchun yetarli.
