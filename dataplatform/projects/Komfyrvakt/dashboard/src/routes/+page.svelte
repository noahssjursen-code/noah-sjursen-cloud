<script lang="ts">
  import { onMount } from 'svelte';
  import LogViewer from '../components/LogViewer.svelte';
  import FilterPanel from '../components/FilterPanel.svelte';
  
  let apiKey = '';
  let isAuthenticated = false;
  
  onMount(() => {
    // Check for saved API key in localStorage
    const saved = localStorage.getItem('komfyrvakt_api_key');
    if (saved) {
      apiKey = saved;
      isAuthenticated = true;
    }
  });
  
  function handleLogin() {
    if (apiKey.startsWith('kmf_')) {
      localStorage.setItem('komfyrvakt_api_key', apiKey);
      isAuthenticated = true;
    }
  }
  
  function handleLogout() {
    localStorage.removeItem('komfyrvakt_api_key');
    apiKey = '';
    isAuthenticated = false;
  }
</script>

<div class="container mx-auto px-4 py-8">
  <!-- Header -->
  <div class="mb-8">
    <h1 class="text-4xl font-bold text-gray-900 mb-2">
      🔥 Komfyrvakt
    </h1>
    <p class="text-gray-600">Simple logging service with AI analytics</p>
  </div>

  {#if !isAuthenticated}
    <!-- Login Form -->
    <div class="max-w-md mx-auto mt-16">
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-2xl font-semibold mb-4">Enter API Key</h2>
        <p class="text-gray-600 mb-4">
          Enter your Komfyrvakt API key to view logs.
        </p>
        
        <form on:submit|preventDefault={handleLogin}>
          <input
            type="text"
            bind:value={apiKey}
            placeholder="kmf_your_api_key_here"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500 focus:border-transparent mb-4"
          />
          <button
            type="submit"
            class="w-full bg-orange-600 text-white py-2 px-4 rounded-md hover:bg-orange-700 transition"
          >
            Continue
          </button>
        </form>
        
        <p class="text-sm text-gray-500 mt-4">
          Find your API key in the terminal output when you first ran Komfyrvakt.
        </p>
      </div>
    </div>
  {:else}
    <!-- Dashboard -->
    <div class="flex justify-between items-center mb-6">
      <div class="flex gap-4 items-center">
        <span class="text-sm text-gray-600">Connected</span>
        <span class="w-2 h-2 bg-green-500 rounded-full"></span>
      </div>
      <button
        on:click={handleLogout}
        class="text-sm text-gray-600 hover:text-gray-900"
      >
        Logout
      </button>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- Filters -->
      <div class="lg:col-span-1">
        <FilterPanel />
      </div>
      
      <!-- Log Viewer -->
      <div class="lg:col-span-3">
        <LogViewer {apiKey} />
      </div>
    </div>
  {/if}
</div>

