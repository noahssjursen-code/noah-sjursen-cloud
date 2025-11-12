<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchGroups } from '../lib/api';
  
  export let apiKey: string;
  export let selectedGroup: string;
  export let onGroupSelect: (group: string) => void;
  
  let groups: string[] = [];
  let loading = false;
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
    // No auto-refresh for groups - only manual refresh
  });
  
  function handleGroupClick(group: string) {
    if (selectedGroup === group) {
      onGroupSelect(''); // Deselect
    } else {
      onGroupSelect(group);
    }
  }
</script>

<div class="h-full flex flex-col">
  <!-- Header -->
  <div class="flex-none px-4 py-3 border-b border-gray-200">
    <div class="flex items-center justify-between">
      <h3 class="text-sm font-semibold text-gray-900">Groups</h3>
      <button
        on:click={loadGroups}
        disabled={loading}
        class="text-xs text-gray-600 hover:text-gray-900 disabled:opacity-50"
      >
        ↻
      </button>
    </div>
  </div>
  
  <!-- Groups List -->
  <div class="flex-1 overflow-y-auto">
    {#if error}
      <div class="px-4 py-3">
        <p class="text-xs text-red-600">{error}</p>
      </div>
    {:else if loading && groups.length === 0}
      <div class="px-4 py-8 text-center">
        <div class="inline-block animate-spin rounded-full h-6 w-6 border-2 border-gray-300 border-t-purple-600"></div>
      </div>
    {:else if groups.length === 0}
      <div class="px-4 py-8 text-center text-xs text-gray-500">
        No groups yet
      </div>
    {:else}
      <div class="py-2">
        <!-- All Logs Option -->
        <button
          on:click={() => handleGroupClick('')}
          class="w-full px-4 py-2 text-left text-sm transition {selectedGroup === '' ? 'bg-purple-50 text-purple-700 font-medium border-l-3 border-l-purple-600' : 'text-gray-700 hover:bg-gray-50'}"
        >
          <div class="flex items-center gap-2">
            <span>📋</span>
            <span>All Logs</span>
          </div>
        </button>
        
        <!-- Group Items -->
        {#each groups as group}
          <button
            on:click={() => handleGroupClick(group)}
            class="w-full px-4 py-2 text-left text-sm transition {selectedGroup === group ? 'bg-purple-50 text-purple-700 font-medium border-l-3 border-l-purple-600' : 'text-gray-700 hover:bg-gray-50'}"
          >
            <div class="flex items-center gap-2">
              <span>📁</span>
              <span class="font-mono truncate">{group}</span>
            </div>
          </button>
        {/each}
      </div>
    {/if}
  </div>
  
  <!-- Footer -->
  <div class="flex-none px-4 py-2 border-t border-gray-200 bg-gray-50">
    <p class="text-xs text-gray-600 text-center">
      {groups.length} group{groups.length !== 1 ? 's' : ''}
    </p>
  </div>
</div>
