<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fetchLogs, type StoredLog } from '../lib/api';
  
  export let apiKey: string;
  export let group: string | undefined = undefined;
  export let minimal: boolean = false;  // Compact view mode
  
  let logs: StoredLog[] = [];
  let loading = false;
  let error = '';
  let autoRefresh = false;  // DISABLED by default
  let searchTerm = '';
  let selectedLevel: string = '';
  let refreshInterval: number;
  
  async function loadLogs() {
    try {
      loading = true;
      error = '';
      logs = await fetchLogs(apiKey, { group, limit: 100 });
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to load logs';
    } finally {
      loading = false;
    }
  }
  
  onMount(() => {
    loadLogs();
  });
  
  onDestroy(() => {
    if (refreshInterval) clearInterval(refreshInterval);
  });
  
  // Toggle auto-refresh
  function toggleAutoRefresh() {
    autoRefresh = !autoRefresh;
    if (refreshInterval) clearInterval(refreshInterval);
    if (autoRefresh) {
      refreshInterval = setInterval(loadLogs, 5000);
    }
  }
  
  // This runs when parent changes the group prop
  export function refresh() {
    loadLogs();
  }
  
  // Compute filtered logs (memoized)
  $: filteredLogs = (() => {
    if (!logs.length) return [];
    return logs.filter(log => {
      const matchesSearch = !searchTerm || 
        log.message.toLowerCase().includes(searchTerm.toLowerCase()) ||
        log.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
      const matchesLevel = !selectedLevel || log.level === selectedLevel;
      return matchesSearch && matchesLevel;
    });
  })();
  
  function getLevelColor(level: string): string {
    switch (level) {
      case 'critical': return 'bg-red-600 text-white';
      case 'error': return 'bg-red-500 text-white';
      case 'warning': return 'bg-yellow-500 text-white';
      case 'info': return 'bg-blue-500 text-white';
      case 'debug': return 'bg-gray-500 text-white';
      default: return 'bg-gray-400 text-white';
    }
  }
</script>

<div class="h-full flex flex-col bg-white">
  <!-- Toolbar -->
  <div class="flex-none px-6 py-2 bg-gray-100 border-b-2 border-gray-300">
    <div class="flex items-center justify-between gap-4">
      <div class="flex items-center gap-2">
        <span class="text-sm font-bold text-gray-700 uppercase tracking-wide">📋 Recent Logs</span>
        <span class="text-xs text-gray-500">({filteredLogs.length} of {logs.length})</span>
      </div>
      
      <div class="flex items-center gap-2">
        {#if !minimal}
          <!-- Search -->
          <div class="relative">
            <input
              type="text"
              bind:value={searchTerm}
              placeholder="Search..."
              class="w-48 px-3 py-1 pl-8 text-xs border border-gray-300 rounded-md focus:ring-2 focus:ring-purple-500"
            />
            <span class="absolute left-2 top-1.5 text-gray-400 text-xs">🔍</span>
          </div>
          
          <!-- Level Filter -->
          <select
            bind:value={selectedLevel}
            class="px-2 py-1 text-xs border border-gray-300 rounded-md focus:ring-2 focus:ring-purple-500"
          >
            <option value="">All</option>
            <option value="error">Errors</option>
            <option value="warning">Warnings</option>
          </select>
        {/if}
        
        <!-- Manual Refresh -->
        <button
          on:click={loadLogs}
          disabled={loading}
          class="px-3 py-1 text-xs bg-gray-200 hover:bg-gray-300 rounded-md transition disabled:opacity-50 font-medium"
        >
          ↻
        </button>
      </div>
    </div>
  </div>
  
  <!-- Logs Content -->
  <div class="flex-1 overflow-y-auto">
    {#if error}
      <div class="p-6">
        <div class="bg-red-50 border border-red-200 rounded-lg p-4">
          <p class="text-red-800 text-sm">{error}</p>
        </div>
      </div>
    {:else if loading && logs.length === 0}
      <div class="flex items-center justify-center h-full">
        <div class="text-center">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-gray-200 border-t-purple-600 mb-2"></div>
          <p class="text-gray-600 text-sm">Loading logs...</p>
        </div>
      </div>
    {:else if filteredLogs.length === 0}
      <div class="flex items-center justify-center h-full">
        <div class="text-center text-gray-500">
          <p class="text-lg font-medium">No logs found</p>
          <p class="text-sm mt-1">Try adjusting your filters or post some logs</p>
        </div>
      </div>
    {:else}
      <div class="divide-y divide-gray-100">
        {#each filteredLogs.slice(0, minimal ? 20 : 100) as log}
          <div class="px-4 py-2 hover:bg-gray-50 transition">
            <div class="flex items-center gap-3 text-xs">
              <!-- Level Badge -->
              <span class="flex-shrink-0 px-2 py-0.5 text-xs font-bold rounded {getLevelColor(log.level)} uppercase">
                {log.level.substring(0, 4)}
              </span>
              
              <!-- Time -->
              <span class="flex-shrink-0 text-gray-500 font-mono w-24">
                {new Date(log.timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
              </span>
              
              <!-- Message -->
              <p class="flex-1 text-gray-900 truncate">{log.message}</p>
              
              <!-- Tags -->
              {#if log.tags.length > 0 && !minimal}
                <div class="flex gap-1">
                  {#each log.tags.slice(0, 2) as tag}
                    <span class="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full">#{tag}</span>
                  {/each}
                </div>
              {/if}
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
  
  <!-- Footer -->
  {#if !minimal}
    <div class="flex-none px-6 py-2 bg-gray-50 border-t border-gray-200">
      <p class="text-xs text-gray-600 text-center">
        Showing {filteredLogs.length} of {logs.length} logs
      </p>
    </div>
  {/if}
</div>
