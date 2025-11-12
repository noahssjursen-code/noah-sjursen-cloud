<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchGroups } from '../lib/api';
  
  export let apiKey: string;
  export let onGroupSelect: (group: string) => void;
  export let selectedGroup: string = '';
  
  let groups: string[] = [];
  let loading = true;
  let error = '';
  
  async function loadGroups() {
    try {
      loading = true;
      error = '';
      groups = await fetchGroups(apiKey);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to load groups';
    } finally {
      loading = false;
    }
  }
  
  onMount(() => {
    loadGroups();
  });
</script>

<div class="bg-white rounded-lg shadow-md p-6">
  <div class="flex justify-between items-center mb-4">
    <h3 class="text-lg font-semibold">Groups</h3>
    <button
      on:click={loadGroups}
      class="text-sm text-gray-600 hover:text-gray-900"
      disabled={loading}
    >
      {loading ? '...' : '↻'}
    </button>
  </div>
  
  {#if error}
    <p class="text-sm text-red-600">{error}</p>
  {:else if loading}
    <p class="text-sm text-gray-500">Loading groups...</p>
  {:else if groups.length === 0}
    <p class="text-sm text-gray-500">No groups found. Logs without groups won't appear here.</p>
  {:else}
    <div class="space-y-1 max-h-96 overflow-y-auto">
      <!-- All logs option -->
      <button
        on:click={() => onGroupSelect('')}
        class="w-full text-left px-3 py-2 rounded text-sm transition {selectedGroup === '' ? 'bg-orange-100 text-orange-900 font-medium' : 'hover:bg-gray-100 text-gray-700'}"
      >
        📋 All Logs
      </button>
      
      <!-- Group list -->
      {#each groups as group}
        <button
          on:click={() => onGroupSelect(group)}
          class="w-full text-left px-3 py-2 rounded text-sm transition font-mono {selectedGroup === group ? 'bg-orange-100 text-orange-900 font-medium' : 'hover:bg-gray-100 text-gray-700'}"
        >
          📁 {group}
        </button>
      {/each}
    </div>
    
    <div class="mt-4 pt-4 border-t border-gray-200">
      <p class="text-xs text-gray-500">{groups.length} group{groups.length !== 1 ? 's' : ''}</p>
    </div>
  {/if}
</div>

