# luna frontend

tauri + react frontend for the luna desktop agent.

## structure

```
src/
├── components/
│   └── Spotlight.tsx    # main ui - input, plan display, execution status
├── utils/
│   └── api.ts           # http client for backend communication
├── App.tsx              # root component
├── App.css              # tailwind styles
└── main.tsx             # react entry point

src-tauri/
├── src/
│   ├── lib.rs           # tauri library
│   └── main.rs          # tauri entry point
└── tauri.conf.json      # tauri configuration
```

## running

```bash
# install dependencies
npm install

# development mode
npm run tauri dev

# build for production
npm run tauri build
```

## requirements

- node.js 18+
- rust (latest stable)
- backend running on localhost:8000

## configuration

api base url is defined in `src/utils/api.ts`:

```typescript
const API_BASE_URL = "http://localhost:8000";
```

## dependencies

- react 18
- typescript
- tailwind css
- lucide-react (icons)
- tauri 2.0
