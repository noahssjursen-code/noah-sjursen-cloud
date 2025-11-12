<script lang="ts">
  import { analyzeLog, type AnalysisResult } from '../lib/api';
  
  export let apiKey: string;
  export let group: string | undefined = undefined;
  
  let analysis: AnalysisResult | null = null;
  let loading = false;
  let error = '';
  let cached = false;
  
  async function runAnalysis(refresh: boolean = false) {
    try {
      loading = true;
      error = '';
      const response = await analyzeLog(apiKey, group, refresh);
      analysis = response.analysis;
      cached = response.cached;
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to analyze logs';
    } finally {
      loading = false;
    }
  }
  
  // Auto-run on mount or when group changes
  $: if (group !== undefined || group === undefined) {
    runAnalysis();
  }
</script>

<div class="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg shadow-md p-6">
  <div class="flex justify-between items-center mb-4">
    <h3 class="text-lg font-semibold text-gray-900">🤖 AI Analysis</h3>
    <div class="flex gap-2">
      {#if cached}
        <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Cached</span>
      {/if}
      <button
        on:click={() => runAnalysis(true)}
        disabled={loading}
        class="text-sm px-3 py-1 bg-white border border-gray-300 rounded hover:bg-gray-50 transition disabled:opacity-50"
      >
        {loading ? 'Analyzing...' : '↻ Refresh'}
      </button>
    </div>
  </div>
  
  {#if error}
    <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded">
      <p class="text-red-800 text-sm">{error}</p>
      <p class="text-red-600 text-xs mt-1">Make sure GEMINI_API_KEY is set in your environment</p>
    </div>
  {:else if loading}
    <div class="text-center py-8">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-purple-200 border-t-purple-600"></div>
      <p class="text-gray-600 mt-2">Analyzing logs with AI...</p>
    </div>
  {:else if analysis}
    <!-- Aggregated Stats -->
    <div class="grid grid-cols-3 gap-4 mb-6">
      <div class="bg-white rounded-lg p-4 shadow-sm">
        <p class="text-sm text-gray-600">Total Logs</p>
        <p class="text-2xl font-bold text-gray-900">{analysis.aggregation.total_logs}</p>
      </div>
      <div class="bg-white rounded-lg p-4 shadow-sm">
        <p class="text-sm text-gray-600">Errors</p>
        <p class="text-2xl font-bold text-red-600">
          {analysis.aggregation.level_counts.error || 0}
        </p>
      </div>
      <div class="bg-white rounded-lg p-4 shadow-sm">
        <p class="text-sm text-gray-600">Warnings</p>
        <p class="text-2xl font-bold text-yellow-600">
          {analysis.aggregation.level_counts.warning || 0}
        </p>
      </div>
    </div>
    
    <!-- Data Field Aggregations -->
    {#if Object.keys(analysis.aggregation.data_fields).length > 0}
      <div class="bg-white rounded-lg p-4 shadow-sm mb-6">
        <h4 class="text-sm font-semibold text-gray-700 mb-3">Data Aggregations</h4>
        <div class="grid grid-cols-2 gap-4">
          {#each Object.entries(analysis.aggregation.data_fields) as [field, stats]}
            <div class="border border-gray-200 rounded p-3">
              <p class="text-sm font-medium text-gray-700 mb-1">{field}</p>
              {#if stats.avg !== undefined}
                <div class="text-xs text-gray-600 space-y-0.5">
                  <p>Min: <span class="font-mono">{stats.min.toFixed(2)}</span></p>
                  <p>Avg: <span class="font-mono">{stats.avg.toFixed(2)}</span></p>
                  <p>Max: <span class="font-mono">{stats.max.toFixed(2)}</span></p>
                  <p class="text-gray-400">({stats.count} values)</p>
                </div>
              {:else if stats.unique_values}
                <div class="text-xs text-gray-600">
                  <p>{stats.unique_values.length} unique value{stats.unique_values.length !== 1 ? 's' : ''}</p>
                  <p class="text-gray-400">({stats.count} total)</p>
                </div>
              {:else}
                <p class="text-xs text-gray-600">{stats.count} occurrence{stats.count !== 1 ? 's' : ''}</p>
              {/if}
            </div>
          {/each}
        </div>
      </div>
    {/if}
    
    <!-- AI Insights -->
    <div class="bg-white rounded-lg p-4 shadow-sm">
      <h4 class="text-sm font-semibold text-gray-700 mb-3">💡 AI Insights</h4>
      <div class="prose prose-sm max-w-none">
        <p class="text-gray-700 whitespace-pre-wrap">{analysis.ai_insights}</p>
      </div>
      <p class="text-xs text-gray-400 mt-3">
        Analyzed {analysis.analyzed_logs} logs at {new Date(analysis.timestamp).toLocaleString()}
      </p>
    </div>
  {/if}
</div>

