<script>
	let output = '';
	
	async function testApi() {
		const response = await fetch('/api');
		const data = await response.json();
		output = JSON.stringify(data, null, 2);
	}
</script>

<main>
	<h1>🎛️ Cloud Control Center</h1>
	<p>GCP Management Dashboard</p>
	
	<button on:click={testApi}>Test API</button>
	
	{#if output}
		<pre>{output}</pre>
	{/if}
</main>

<style>
	main {
		padding: 2rem;
		font-family: sans-serif;
	}
	
	h1 {
		color: #333;
	}
	
	button {
		padding: 0.5rem 1rem;
		background: #4285f4;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}
	
	button:hover {
		background: #357ae8;
	}
	
	pre {
		background: #f5f5f5;
		padding: 1rem;
		border-radius: 4px;
		margin-top: 1rem;
	}
</style>

