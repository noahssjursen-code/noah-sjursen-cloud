# SvelteKit Apps - Standard Pattern

## Project Structure

```
project-name/
├── dashboard/                 # SvelteKit app
│   ├── src/
│   │   ├── app.html          # HTML shell
│   │   ├── app.css           # Tailwind imports
│   │   ├── routes/           # Pages
│   │   │   ├── +layout.svelte # Root layout (imports app.css)
│   │   │   └── +page.svelte  # Root page
│   │   ├── components/       # Reusable components (if needed)
│   │   └── lib/              # Utilities
│   ├── package.json
│   ├── svelte.config.js      # Adapter configuration
│   ├── vite.config.js
│   ├── tailwind.config.js    # Tailwind configuration
│   ├── postcss.config.js     # PostCSS configuration
│   └── tsconfig.json         # TypeScript config
└── api/                       # FastAPI backend (mounts this)
```

## Adapter Configuration

Always use `@sveltejs/adapter-static` for FastAPI mounting:

```javascript
import adapter from '@sveltejs/adapter-static';

export default {
	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: 'index.html',
			precompress: false,
			strict: true
		})
	}
};
```

## Package.json Scripts

```json
{
  "scripts": {
    "dev": "vite dev",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

## Dependencies

Required:

```json
{
  "devDependencies": {
    "@sveltejs/adapter-static": "^3.0.0",
    "@sveltejs/kit": "^2.0.0",
    "@sveltejs/vite-plugin-svelte": "^3.0.0",
    "svelte": "^4.2.0",
    "vite": "^5.0.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}
```

## API Communication

Fetch from `/api` endpoints (served by FastAPI):

```svelte
<script>
	async function callApi() {
		const response = await fetch('/api/endpoint');
		const data = await response.json();
		return data;
	}
</script>
```

## Building

Build creates static files in `build/` directory:

```bash
npm run build
```

FastAPI serves these files:

```python
app.mount("/", StaticFiles(directory="dashboard/build", html=True), name="dashboard")
```

## File Naming Conventions

- Pages: `+page.svelte`
- Layouts: `+layout.svelte`
- Server endpoints: `+server.ts` (avoid - use FastAPI instead)
- Components: `ComponentName.svelte` (PascalCase)

## Styling with TailwindCSS

### Setup Required Files

**`tailwind.config.js`:**
```javascript
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {}
	},
	plugins: []
};
```

**`postcss.config.js`:**
```javascript
export default {
	plugins: {
		tailwindcss: {},
		autoprefixer: {}
	}
};
```

**`src/app.css`:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Import in `src/routes/+layout.svelte`:**
```svelte
<script>
	import '../app.css';
</script>

<slot />
```

### Usage

Use Tailwind classes directly:

```svelte
<div class="flex items-center justify-center p-4">
	<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
		Click me
	</button>
</div>
```

Component-specific styles (if needed):

```svelte
<style>
	.custom {
		/* Only for truly custom styles not in Tailwind */
	}
</style>
```

## TypeScript

Use `.ts` files for utilities, `.svelte` for components.

Type your props:

```svelte
<script lang="ts">
	export let title: string;
	export let count: number = 0;
</script>
```

## Common Patterns

### Loading States

```svelte
<script>
	let loading = false;
	let data = null;
	
	async function load() {
		loading = true;
		data = await fetch('/api/data').then(r => r.json());
		loading = false;
	}
</script>

{#if loading}
	<p class="text-gray-500">Loading...</p>
{:else if data}
	<p class="text-lg font-semibold">{data.value}</p>
{/if}
```

### Forms

```svelte
<script>
	let value = '';
	
	async function submit() {
		await fetch('/api/submit', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ value })
		});
	}
</script>

<form on:submit|preventDefault={submit} class="space-y-4">
	<input bind:value class="border border-gray-300 rounded px-3 py-2 w-full" />
	<button class="bg-blue-500 hover:bg-blue-700 text-white px-4 py-2 rounded">
		Submit
	</button>
</form>
```

## Do Not

- Do not use SvelteKit server routes (`+server.ts`) - use FastAPI
- Do not use SSR features - static adapter only
- Do not put business logic in Svelte - keep in FastAPI
- Do not commit `node_modules/` or `build/`
- Do not skip TailwindCSS - always use it for styling

