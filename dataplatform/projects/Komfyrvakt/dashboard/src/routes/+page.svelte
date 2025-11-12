<script lang="ts">
  import { onMount } from 'svelte';
  import LogViewer from '../components/LogViewer.svelte';
  import GroupList from '../components/GroupList.svelte';
  import AnalysisPanel from '../components/AnalysisPanel.svelte';
  
  // Auto-load API key from build-time environment variable or localStorage
  let apiKey = import.meta.env.VITE_API_KEY || '';
  let isAuthenticated = !!apiKey;
  let selectedGroup = '';
  
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
  
  let logViewerRef: any;
  let analysisPanelRef: any;
  
  function handleGroupSelect(group: string) {
    selectedGroup = group;
    // Manually trigger refresh on components
    if (logViewerRef) logViewerRef.refresh();
    if (analysisPanelRef) analysisPanelRef.refresh();
  }
</script>

<div class="h-screen w-full overflow-hidden bg-gray-50 flex flex-col">

  {#if !isAuthenticated}
    <!-- No API Key Found -->
    <div class="flex items-center justify-center h-full">
      <div class="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
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
    <!-- Header Bar -->
    <div class="flex-none bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
      <div class="flex items-center gap-4">
        <h1 class="text-xl font-bold text-gray-900">🔥 Komfyrvakt</h1>
        {#if selectedGroup}
          <span class="text-sm text-gray-500">•</span>
          <span class="text-sm font-mono text-orange-600">{selectedGroup}</span>
        {/if}
      </div>
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 bg-green-500 rounded-full"></span>
        <span class="text-xs text-gray-600">Live</span>
      </div>
    </div>
    
    <!-- Main Content Area -->
    <div class="flex-1 flex overflow-hidden">
      <!-- Sidebar -->
      <div class="flex-none w-64 bg-white border-r border-gray-200 overflow-y-auto">
        <GroupList {apiKey} {selectedGroup} onGroupSelect={handleGroupSelect} />
      </div>
      
      <!-- Main Content (HORIZONTAL) -->
      <div class="flex-1 flex overflow-hidden">
        <!-- AI Analysis & Metrics (LEFT - 70%) -->
        <div class="flex-1 overflow-y-auto bg-white">
          <AnalysisPanel bind:this={analysisPanelRef} {apiKey} group={selectedGroup || undefined} />
        </div>
        
        <!-- Logs Panel (RIGHT - 30%) -->
        <div class="flex-none w-96 border-l-2 border-gray-300 overflow-hidden bg-gray-50">
          <LogViewer bind:this={logViewerRef} {apiKey} group={selectedGroup || undefined} minimal={true} />
        </div>
      </div>
    </div>
  {/if}
</div>

