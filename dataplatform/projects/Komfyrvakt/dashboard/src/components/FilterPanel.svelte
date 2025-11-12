<script lang="ts">
  // Placeholder for filtering controls
  let selectedGroup = '';
  let selectedLevel = 'all';
  let selectedTags: string[] = [];
</script>

<div class="bg-white rounded-lg shadow-md p-6">
  <h3 class="text-lg font-semibold mb-4">Filters</h3>
  
  <!-- Group Filter -->
  <div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 mb-1">
      Group
    </label>
    <input
      type="text"
      bind:value={selectedGroup}
      placeholder="restaurant-a:*"
      class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-orange-500 focus:border-transparent"
    />
    <p class="text-xs text-gray-500 mt-1">Use * for prefix match</p>
  </div>
  
  <!-- Level Filter -->
  <div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 mb-1">
      Level
    </label>
    <select
      bind:value={selectedLevel}
      class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-orange-500 focus:border-transparent"
    >
      <option value="all">All Levels</option>
      <option value="debug">Debug</option>
      <option value="info">Info</option>
      <option value="warning">Warning</option>
      <option value="error">Error</option>
      <option value="critical">Critical</option>
    </select>
  </div>
  
  <!-- Tags Filter -->
  <div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 mb-1">
      Tags
    </label>
    <input
      type="text"
      placeholder="temperature,alert"
      class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-orange-500 focus:border-transparent"
    />
    <p class="text-xs text-gray-500 mt-1">Comma-separated</p>
  </div>
  
  <!-- Apply Button -->
  <button
    class="w-full bg-orange-600 text-white py-2 px-4 rounded-md hover:bg-orange-700 transition text-sm font-medium"
  >
    Apply Filters
  </button>
  
  <button
    class="w-full mt-2 bg-gray-100 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-200 transition text-sm"
  >
    Clear Filters
  </button>
  
  <!-- Quick Stats -->
  <div class="mt-6 pt-6 border-t border-gray-200">
    <h4 class="text-sm font-medium text-gray-700 mb-2">Quick Stats</h4>
    <div class="space-y-2 text-sm text-gray-600">
      <div class="flex justify-between">
        <span>Total Logs:</span>
        <span class="font-mono">-</span>
      </div>
      <div class="flex justify-between">
        <span>Retention:</span>
        <span class="font-mono">48h</span>
      </div>
    </div>
  </div>
</div>

