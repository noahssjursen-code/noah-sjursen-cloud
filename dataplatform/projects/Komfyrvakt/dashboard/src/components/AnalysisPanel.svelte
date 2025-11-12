<script lang="ts">
  import { onMount } from 'svelte';
  import { analyzeLog, type AnalysisResult, type AIInsights } from '../lib/api';
  import TimeSeriesChart from './TimeSeriesChart.svelte';
  
  export let apiKey: string;
  export let group: string | undefined = undefined;
  
  let analysis: AnalysisResult | null = null;
  let loading = false;
  let error = '';
  let cached = false;
  let showCharts = false;  // Expandable chart panel
  
  async function runAnalysis(refresh: boolean = false) {
    try {
      loading = true;
      error = '';
      const response = await analyzeLog(apiKey, group, refresh);
      analysis = response.analysis;
      cached = response.cached;
      console.log('Analysis received:', analysis);
      console.log('Time series:', analysis?.time_series);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to analyze logs';
    } finally {
      loading = false;
    }
  }
  
  onMount(() => {
    runAnalysis(false);  // Use cache on initial load
  });
  
  // Export refresh method for parent to call
  export function refresh() {
    runAnalysis(false);  // Parent refresh should use cache too
  }
  
  function isAIInsights(insights: any): insights is AIInsights {
    return insights && typeof insights === 'object' && 'summary' in insights;
  }
  
  function getSeverityColor(severity: string): string {
    switch (severity) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-300';
      case 'warning': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'medium': return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'low': return 'bg-gray-100 text-gray-800 border-gray-300';
      case 'info': return 'bg-blue-50 text-blue-700 border-blue-200';
      default: return 'bg-green-100 text-green-800 border-green-300';
    }
  }
</script>

<div class="h-full flex flex-col bg-gradient-to-br from-slate-50 to-gray-100">
  <!-- Header -->
  <div class="flex-none px-6 py-4 bg-white border-b-2 border-gray-200">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-gradient-to-br from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
          <span class="text-2xl">🤖</span>
        </div>
        <div>
          <h2 class="text-xl font-bold text-gray-900">AI Analysis & Insights</h2>
          <p class="text-xs text-gray-600">Time series analysis with trend detection</p>
        </div>
        {#if cached}
          <span class="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium border border-green-300">✓ Cached</span>
        {/if}
      </div>
      <button
        on:click={() => runAnalysis(true)}
        disabled={loading}
        class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium shadow-sm"
      >
        {loading ? '⟳ Analyzing...' : '↻ Refresh Analysis'}
      </button>
    </div>
  </div>
  
  <!-- Content -->
  <div class="flex-1 overflow-y-auto p-6">
    {#if error}
      <div class="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg shadow-sm">
        <p class="text-red-800 text-sm font-medium">{error}</p>
        <p class="text-red-600 text-xs mt-2">Make sure GEMINI_API_KEY is set in your environment</p>
      </div>
    {:else if loading}
      <div class="flex flex-col items-center justify-center py-20">
        <div class="inline-block animate-spin rounded-full h-16 w-16 border-4 border-purple-200 border-t-purple-600 mb-4"></div>
        <p class="text-gray-700 font-semibold text-lg">Loading analysis...</p>
        <p class="text-gray-500 text-sm mt-2">Fetching insights and metrics</p>
      </div>
    {:else if analysis}
      <div class="space-y-6">
        
        <!-- Summary Card -->
        {#if isAIInsights(analysis.ai_insights)}
          <div class="bg-white rounded-xl p-6 shadow-md border-2 {analysis.ai_insights.severity === 'critical' ? 'border-red-400' : analysis.ai_insights.severity === 'warning' ? 'border-yellow-400' : 'border-green-400'}">
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0 w-12 h-12 rounded-full {getSeverityColor(analysis.ai_insights.severity)} flex items-center justify-center border-2 text-lg font-bold">
                {analysis.ai_insights.severity === 'critical' ? '!' : analysis.ai_insights.severity === 'warning' ? '⚠' : '✓'}
              </div>
              <div class="flex-1">
                <div class="flex items-center justify-between mb-2">
                  <h3 class="text-sm font-bold text-gray-700 uppercase tracking-wide">System Health Status</h3>
                  <span class="text-xs font-semibold px-3 py-1 rounded-full {getSeverityColor(analysis.ai_insights.severity)}">
                    {analysis.ai_insights.severity.toUpperCase()}
                  </span>
                </div>
                <p class="text-gray-900 text-lg leading-relaxed">{analysis.ai_insights.summary}</p>
              </div>
            </div>
          </div>
        {/if}
        
        <!-- Stats Grid -->
        <div class="grid grid-cols-4 gap-4">
          <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <p class="text-xs text-gray-600 font-bold uppercase tracking-wider mb-1">Total Logs</p>
            <p class="text-3xl font-bold text-gray-900">{analysis.aggregation.total_logs}</p>
          </div>
          <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <p class="text-xs text-gray-600 font-bold uppercase tracking-wider mb-1">Errors</p>
            <p class="text-3xl font-bold text-red-600">{analysis.aggregation.level_counts.error || 0}</p>
          </div>
          <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <p class="text-xs text-gray-600 font-bold uppercase tracking-wider mb-1">Warnings</p>
            <p class="text-3xl font-bold text-yellow-600">{analysis.aggregation.level_counts.warning || 0}</p>
          </div>
          <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <p class="text-xs text-gray-600 font-bold uppercase tracking-wider mb-1">Time Intervals</p>
            <p class="text-3xl font-bold text-purple-600">{analysis.time_series?.total_intervals || 0}</p>
          </div>
        </div>
        
        <!-- Time Series Charts (Expandable) -->
        {#if analysis.time_series && analysis.time_series.intervals.length > 0}
          <div class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
            <button
              on:click={() => showCharts = !showCharts}
              class="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition"
            >
              <div class="flex items-center gap-3">
                <span class="text-lg">📈</span>
                <div class="text-left">
                  <h3 class="text-sm font-bold text-gray-700 uppercase tracking-wide">Time Series Trends</h3>
                  <p class="text-xs text-gray-500">{analysis.time_series.total_intervals} intervals • {analysis.time_series.fields_tracked.join(', ')}</p>
                </div>
              </div>
              <span class="text-gray-500 text-xl">{showCharts ? '▼' : '▶'}</span>
            </button>
            
            {#if showCharts}
              <div class="border-t border-gray-200 p-6 bg-gray-50">
                <!-- Chart -->
                <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200 mb-4" style="height: 300px;">
                  <TimeSeriesChart timeSeries={analysis.time_series} />
                </div>
                
                <!-- Data Table -->
                <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
                  <h4 class="text-xs font-bold text-gray-700 uppercase mb-3">Recent Intervals</h4>
                  <div class="space-y-2 max-h-48 overflow-y-auto">
                    {#each analysis.time_series.intervals.slice(-10) as interval}
                      <div class="flex items-center gap-3 p-2 bg-gray-50 rounded text-xs">
                        <span class="flex-shrink-0 font-mono text-gray-600 w-28">
                          {new Date(interval.timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}
                        </span>
                        <span class="text-gray-500">Logs: {interval.log_count}</span>
                        {#each Object.entries(interval.data) as [field, stats]}
                          <span class="text-gray-700">
                            <span class="font-medium text-purple-600">{field}:</span> {stats.avg.toFixed(2)}
                            <span class="text-gray-400 ml-1">({stats.min.toFixed(1)}-{stats.max.toFixed(1)})</span>
                          </span>
                        {/each}
                      </div>
                    {/each}
                  </div>
                </div>
              </div>
            {/if}
          </div>
        {/if}
        
        {#if isAIInsights(analysis.ai_insights)}
          <!-- Findings -->
          {#if analysis.ai_insights.findings.length > 0}
            <div class="bg-white rounded-xl p-6 shadow-md border border-gray-200">
              <h3 class="text-sm font-bold text-gray-700 uppercase tracking-wide mb-4 flex items-center gap-2">
                <span>🔍</span> Key Findings
              </h3>
              <div class="space-y-3">
                {#each analysis.ai_insights.findings as finding}
                  <div class="border-l-4 pl-4 py-3 rounded-r-lg {finding.severity === 'critical' ? 'border-red-500 bg-red-50' : finding.severity === 'warning' ? 'border-yellow-500 bg-yellow-50' : 'border-blue-500 bg-blue-50'}">
                    <div class="flex items-start justify-between gap-2">
                      <h4 class="font-bold text-gray-900">{finding.title}</h4>
                      <span class="text-xs font-bold px-2 py-1 rounded {getSeverityColor(finding.severity)}">
                        {finding.severity.toUpperCase()}
                      </span>
                    </div>
                    <p class="text-sm text-gray-700 mt-2">{finding.description}</p>
                  </div>
                {/each}
              </div>
            </div>
          {/if}
          
          <!-- Recommendations -->
          {#if analysis.ai_insights.recommendations.length > 0}
            <div class="bg-white rounded-xl p-6 shadow-md border border-gray-200">
              <h3 class="text-sm font-bold text-gray-700 uppercase tracking-wide mb-4 flex items-center gap-2">
                <span>💡</span> Recommended Actions
              </h3>
              <div class="space-y-3">
                {#each analysis.ai_insights.recommendations as rec}
                  <div class="flex items-start gap-3 p-4 rounded-lg bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200">
                    <span class="flex-shrink-0 w-8 h-8 rounded-full {getSeverityColor(rec.priority)} flex items-center justify-center text-xs font-bold border-2">
                      {rec.priority === 'high' ? 'H' : rec.priority === 'medium' ? 'M' : 'L'}
                    </span>
                    <p class="text-sm text-gray-900 flex-1 pt-1">{rec.action}</p>
                  </div>
                {/each}
              </div>
            </div>
          {/if}
        {/if}
        
        <!-- Footer -->
        <div class="text-center">
          <p class="text-xs text-gray-500">
            Analyzed {analysis.analyzed_logs} logs across {analysis.time_series?.total_intervals || 0} time intervals • Generated {new Date(analysis.timestamp).toLocaleString()}
          </p>
        </div>
      </div>
    {/if}
  </div>
</div>
