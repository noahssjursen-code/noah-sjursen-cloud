<script lang="ts">
  import { onMount } from 'svelte';
  import LogViewer from '../components/LogViewer.svelte';
  import GroupList from '../components/GroupList.svelte';
  import AnalysisPanel from '../components/AnalysisPanel.svelte';
  
  // Auto-load API key from build-time environment variable or localStorage
  let apiKey = import.meta.env.VITE_API_KEY || '';
  let isAuthenticated = !!apiKey;
  let selectedGroup = '';
  let showAnalysis = false;
  
  onMount(() => {
    // If not in build, try localStorage as fallback
    if (!apiKey) {
      const saved = localStorage.getItem('komfyrvakt_api_key');
      if (saved) {
        apiKey = saved;
        isAuthenticated = true;
      }
    }
  });
  
  function handleGroupSelect(group: string) {
    selectedGroup = group;
    showAnalysis = false;  // Reset analysis when switching groups
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
    <!-- No API Key Found -->
    <div class="max-w-md mx-auto mt-16">
      <div class="bg-red-50 border border-red-200 rounded-lg p-6">
        <h2 class="text-2xl font-semibold text-red-900 mb-4">⚠️ Configuration Error</h2>
        <p class="text-red-800 mb-4">
          API key not found. The dashboard was not built correctly.
        </p>
        <p class="text-sm text-red-700">
          Run: <code class="bg-red-100 px-2 py-1 rounded">.\build-dashboard.ps1</code> to rebuild with API key.
        </p>
      </div>
    </div>
  {:else}
    <!-- Dashboard -->
    <div class="flex justify-end items-center mb-6">
      <div class="flex gap-4 items-center">
        <span class="w-2 h-2 bg-green-500 rounded-full"></span>
        <span class="text-sm text-gray-600">Connected</span>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
      <!-- Groups Sidebar -->
      <div class="lg:col-span-1">
        <GroupList {apiKey} {selectedGroup} onGroupSelect={handleGroupSelect} />
      </div>
      
      <!-- Main Content -->
      <div class="lg:col-span-4">
        <div class="mb-4 flex justify-between items-center">
          <div>
            {#if selectedGroup}
              <h2 class="text-xl font-semibold">Group: <span class="font-mono text-orange-600">{selectedGroup}</span></h2>
            {:else}
              <h2 class="text-xl font-semibold">All Logs</h2>
            {/if}
          </div>
          <button
            on:click={() => showAnalysis = !showAnalysis}
            class="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition text-sm font-medium"
          >
            {showAnalysis ? 'Hide' : 'Show'} AI Analysis
          </button>
        </div>
        
        {#if showAnalysis}
          <div class="mb-6">
            <AnalysisPanel {apiKey} group={selectedGroup || undefined} />
          </div>
        {/if}
        
        <LogViewer {apiKey} group={selectedGroup || undefined} />
      </div>
    </div>
  {/if}
</div>

