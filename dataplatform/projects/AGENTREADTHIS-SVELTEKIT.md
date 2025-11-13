# SvelteKit Apps - Standard Pattern

## Project Structure

```
project-name/
├── dashboard/                 # SvelteKit app
│   ├── src/
│   │   ├── app.html          # HTML shell
│   │   ├── routes/           # Pages
│   │   │   └── +page.svelte  # Root page
│   │   ├── components/       # Reusable components (if needed)
│   │   └── lib/              # Utilities
│   ├── package.json
│   ├── svelte.config.js      # Adapter configuration
│   ├── vite.config.js
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

Minimal required:

```json
{
  "devDependencies": {
    "@sveltejs/adapter-static": "^3.0.0",
    "@sveltejs/kit": "^2.0.0",
    "@sveltejs/vite-plugin-svelte": "^3.0.0",
    "svelte": "^4.2.0",
    "vite": "^5.0.0",
    "typescript": "^5.0.0"
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

## Styling

Inline styles in components:

```svelte
<style>
	.class {
		property: value;
	}
</style>
```

Or TailwindCSS if needed (add separately).

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
	<p>Loading...</p>
{:else if data}
	<p>{data.value}</p>
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

<form on:submit|preventDefault={submit}>
	<input bind:value />
	<button>Submit</button>
</form>
```

## Do Not

- Do not use SvelteKit server routes (`+server.ts`) - use FastAPI
- Do not use SSR features - static adapter only
- Do not put business logic in Svelte - keep in FastAPI
- Do not commit `node_modules/` or `build/`

