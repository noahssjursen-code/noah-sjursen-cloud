<script>
	import { onMount } from 'svelte';
	
	let output = '';
	let loading = false;
	let user = null;
	let checkingAuth = true;
	let errorMessage = '';
	let darkMode = true;
	let activeSection = 'overview';
	let applicationsExpanded = false;
	let resources = null;
	let loadingResources = false;
	let users = [];
	let loadingUsers = false;
	let newUserEmail = '';
	let newUserRole = 'viewer';
	
	onMount(async () => {
		// Load theme preference
		const savedTheme = localStorage.getItem('theme');
		darkMode = savedTheme !== 'light';
		
		// Check for error in URL
		const params = new URLSearchParams(window.location.search);
		if (params.get('error') === 'unauthorized') {
			errorMessage = 'Access denied. Your email is not authorized.';
		}
		
		await checkAuth();
	});
	
	function toggleTheme() {
		darkMode = !darkMode;
		localStorage.setItem('theme', darkMode ? 'dark' : 'light');
	}
	
	async function checkAuth() {
		checkingAuth = true;
		try {
			const response = await fetch('/api/user');
			if (response.ok) {
				user = await response.json();
				// Load resources after auth
				await loadResources();
			}
		} catch (error) {
			user = null;
		} finally {
			checkingAuth = false;
		}
	}
	
	async function loadResources() {
		loadingResources = true;
		try {
			const response = await fetch('/api/resources');
			if (response.ok) {
				resources = await response.json();
			}
		} catch (error) {
			console.error('Failed to load resources:', error);
		} finally {
			loadingResources = false;
		}
	}
	
	async function testApi() {
		loading = true;
		try {
			const response = await fetch('/api');
			const data = await response.json();
			output = JSON.stringify(data, null, 2);
		} catch (error) {
			output = `Error: ${error.message}`;
		} finally {
			loading = false;
		}
	}
	
	function login() {
		window.location.href = '/auth/login';
	}
	
	function logout() {
		window.location.href = '/auth/logout';
	}
	
	async function loadUsers() {
		if (user?.role !== 'admin') return;
		
		loadingUsers = true;
		try {
			const response = await fetch('/api/users');
			if (response.ok) {
				const data = await response.json();
				users = data.users;
			} else {
				console.error('Failed to load users');
			}
		} catch (error) {
			console.error('Error loading users:', error);
		} finally {
			loadingUsers = false;
		}
	}
	
	async function assignRole() {
		if (!newUserEmail || !newUserRole) return;
		
		try {
			const response = await fetch('/api/users/assign-role', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email: newUserEmail, role: newUserRole })
			});
			
			if (response.ok) {
				newUserEmail = '';
				newUserRole = 'viewer';
				await loadUsers();
			} else {
				const error = await response.json();
				alert(`Failed to assign role: ${error.error}`);
			}
		} catch (error) {
			alert(`Error: ${error.message}`);
		}
	}
	
	async function revokeRole(email, role) {
		if (!confirm(`Revoke ${role} role from ${email}?`)) return;
		
		try {
			const response = await fetch('/api/users/revoke-role', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, role })
			});
			
			if (response.ok) {
				await loadUsers();
			} else {
				const error = await response.json();
				alert(`Failed to revoke role: ${error.error}`);
			}
		} catch (error) {
			alert(`Error: ${error.message}`);
		}
	}
	
	// Watch for section changes to load users when switching to user management
	$: if (activeSection === 'user-management' && user?.role === 'admin' && users.length === 0) {
		loadUsers();
	}
</script>

<div class="min-h-screen {darkMode ? 'bg-zinc-950 text-gray-100' : 'bg-gray-50 text-gray-900'}">
	<!-- Header -->
	<div class="{darkMode ? 'border-b border-zinc-800 bg-zinc-900' : 'border-b border-gray-200 bg-white'}">
		<div class="container mx-auto px-6 py-4">
			<div class="flex items-center justify-between">
				<div>
					<h1 class="text-xl font-semibold tracking-tight {darkMode ? 'text-white' : 'text-gray-900'}">
						Cloud Control Center
					</h1>
					<p class="text-sm {darkMode ? 'text-zinc-400' : 'text-gray-600'} mt-1">
						Google Cloud Platform Management
					</p>
				</div>
				<div class="flex items-center gap-4">
					<button 
						on:click={toggleTheme}
						class="{darkMode ? 'text-zinc-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'} transition-colors"
						title="Toggle theme"
					>
						{#if darkMode}
							<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
							</svg>
						{:else}
							<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
							</svg>
						{/if}
					</button>
					{#if checkingAuth}
						<span class="text-xs {darkMode ? 'text-zinc-500' : 'text-gray-500'}">Checking auth...</span>
					{:else if user && user.authenticated}
						<div class="flex items-center gap-3">
							<div class="flex flex-col items-end">
								<span class="text-sm {darkMode ? 'text-zinc-300' : 'text-gray-700'}">{user.email}</span>
								<span class="text-xs {darkMode ? 'text-zinc-600' : 'text-gray-500'} uppercase">
									{user.role || 'viewer'}
								</span>
							</div>
							<button 
								on:click={logout}
								class="text-xs {darkMode ? 'text-zinc-400 hover:text-white' : 'text-gray-600 hover:text-gray-900'} uppercase tracking-wider"
							>
								Logout
							</button>
						</div>
					{:else}
						<button 
							on:click={login}
							class="{darkMode ? 'bg-zinc-800 hover:bg-zinc-700 border-zinc-700' : 'bg-white hover:bg-gray-50 border-gray-300 text-gray-900'} text-xs px-4 py-2 border uppercase tracking-wider"
						>
							Sign In with Google
						</button>
					{/if}
					<span class="text-xs {darkMode ? 'text-zinc-500' : 'text-gray-500'} uppercase tracking-wider">v0.1.0</span>
					<div class="h-2 w-2 rounded-full bg-green-500"></div>
				</div>
			</div>
		</div>
	</div>

	<!-- Main Content -->
	<div class="container mx-auto px-6 py-8">
		{#if errorMessage}
			<!-- Unauthorized Error -->
			<div class="{darkMode ? 'bg-zinc-900 border-red-900' : 'bg-white border-red-300'} border">
				<div class="p-8 flex flex-col items-center justify-center text-center">
					<svg class="w-16 h-16 text-red-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
					</svg>
					<h2 class="text-2xl font-semibold {darkMode ? 'text-white' : 'text-gray-900'} mb-2">
						Access Denied
					</h2>
					<p class="{darkMode ? 'text-zinc-400' : 'text-gray-600'} max-w-md">
						Your account does not have permission to access this system.
						Contact your system administrator to request access.
					</p>
					<button 
						on:click={() => { errorMessage = ''; window.location.href = '/'; }}
						class="mt-6 {darkMode ? 'bg-zinc-800 hover:bg-zinc-700 border-zinc-700' : 'bg-gray-100 hover:bg-gray-200 border-gray-300 text-gray-900'} text-xs px-6 py-3 border uppercase tracking-wider"
					>
						Return
					</button>
				</div>
			</div>
		{:else if !user || !user.authenticated}
			<!-- Not Logged In -->
			<div class="{darkMode ? 'bg-zinc-900 border-zinc-800' : 'bg-white border-gray-200'} border">
				<div class="p-12 flex flex-col items-center justify-center text-center">
					<div class="w-20 h-20 border-2 {darkMode ? 'border-zinc-700' : 'border-gray-300'} rounded-full flex items-center justify-center mb-6">
						<svg class="w-10 h-10 {darkMode ? 'text-zinc-600' : 'text-gray-400'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
						</svg>
					</div>
					<h2 class="text-xl font-medium {darkMode ? 'text-white' : 'text-gray-900'} mb-2">
						Authentication Required
					</h2>
					<p class="{darkMode ? 'text-zinc-400' : 'text-gray-600'} mb-6">
						Sign in with your Google account to access the control center
					</p>
					<button 
						on:click={login}
						class="{darkMode ? 'bg-zinc-800 hover:bg-zinc-700 border-zinc-700 text-white' : 'bg-blue-600 hover:bg-blue-700 border-blue-600 text-white'} px-6 py-3 border uppercase tracking-wider text-sm"
					>
						Sign In with Google
					</button>
				</div>
			</div>
		{:else}
			<!-- Logged In - Show Dashboard with Sidebar -->
			<div class="flex gap-6">
				<!-- Left Sidebar Menu -->
				<div class="w-64 flex-shrink-0">
					<div class="{darkMode ? 'bg-zinc-900 border-zinc-800' : 'bg-white border-gray-200'} border">
						<div class="{darkMode ? 'border-b border-zinc-800' : 'border-b border-gray-200'} px-4 py-3">
							<h2 class="text-xs font-medium {darkMode ? 'text-zinc-500' : 'text-gray-500'} uppercase tracking-wider">
								Navigation
							</h2>
						</div>
						<nav class="p-2">
							<!-- Overview -->
							<button
								on:click={() => activeSection = 'overview'}
								class="w-full text-left px-4 py-2.5 text-sm {activeSection === 'overview' ? (darkMode ? 'bg-zinc-800 text-white' : 'bg-blue-50 text-blue-600') : (darkMode ? 'text-zinc-400 hover:bg-zinc-800 hover:text-white' : 'text-gray-700 hover:bg-gray-100')} transition-colors"
							>
								Overview
							</button>
							
							<!-- User Management -->
							<button
								on:click={() => activeSection = 'users'}
								class="w-full text-left px-4 py-2.5 text-sm {activeSection === 'users' ? (darkMode ? 'bg-zinc-800 text-white' : 'bg-blue-50 text-blue-600') : (darkMode ? 'text-zinc-400 hover:bg-zinc-800 hover:text-white' : 'text-gray-700 hover:bg-gray-100')} transition-colors"
							>
								User Management
							</button>
							
							<!-- Applications (Collapsible) -->
							<div class="mt-2">
								<button
									on:click={() => applicationsExpanded = !applicationsExpanded}
									class="w-full text-left px-4 py-2.5 text-sm {darkMode ? 'text-zinc-400 hover:bg-zinc-800 hover:text-white' : 'text-gray-700 hover:bg-gray-100'} transition-colors flex items-center justify-between"
								>
									<span>Applications</span>
									<svg class="w-4 h-4 transition-transform {applicationsExpanded ? 'rotate-90' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
									</svg>
								</button>
								
								{#if applicationsExpanded}
									<div class="ml-4 mt-1 space-y-1">
										<div class="px-4 py-2 text-xs {darkMode ? 'text-zinc-600' : 'text-gray-500'} italic">
											No applications yet
										</div>
									</div>
								{/if}
							</div>
						</nav>
					</div>
				</div>

				<!-- Main Content Area -->
				<div class="flex-1">
					{#if activeSection === 'overview'}
						<!-- Overview Section -->
						<div class="grid gap-6">
							<!-- Resource Stats -->
							{#if loadingResources}
								<div class="{darkMode ? 'bg-zinc-900 border-zinc-800' : 'bg-white border-gray-200'} border p-8 text-center">
									<p class="text-sm {darkMode ? 'text-zinc-400' : 'text-gray-600'}">Loading resources...</p>
								</div>
							{:else if resources && resources.success}
								<div class="grid grid-cols-3 gap-4">
									<!-- Compute Instances -->
									<div class="{darkMode ? 'bg-zinc-900 border-zinc-800' : 'bg-white border-gray-200'} border p-6">
										<div class="text-xs {darkMode ? 'text-zinc-500' : 'text-gray-500'} uppercase tracking-wider mb-2">
											Compute Engine
										</div>
										<div class="text-3xl font-bold {darkMode ? 'text-white' : 'text-gray-900'}">
											{resources.counts.compute_instances}
										</div>
										<div class="text-xs {darkMode ? 'text-zinc-600' : 'text-gray-500'} mt-1">
											Instances
										</div>
									</div>
									
									<!-- Cloud Run -->
									<div class="{darkMode ? 'bg-zinc-900 border-zinc-800' : 'bg-white border-gray-200'} border p-6">
										<div class="text-xs {darkMode ? 'text-zinc-500' : 'text-gray-500'} uppercase tracking-wider mb-2">
											Cloud Run
										</div>
										<div class="text-3xl font-bold {darkMode ? 'text-white' : 'text-gray-900'}">
											{resources.counts.cloud_run_services}
										</div>
										<div class="text-xs {darkMode ? 'text-zinc-600' : 'text-gray-500'} mt-1">
											Services
										</div>
									</div>
									
									<!-- Storage -->
									<div class="{darkMode ? 'bg-zinc-900 border-zinc-800' : 'bg-white border-gray-200'} border p-6">
										<div class="text-xs {darkMode ? 'text-zinc-500' : 'text-gray-500'} uppercase tracking-wider mb-2">
											Cloud Storage
										</div>
										<div class="text-3xl font-bold {darkMode ? 'text-white' : 'text-gray-900'}">
											{resources.counts.storage_buckets}
										</div>
										<div class="text-xs {darkMode ? 'text-zinc-600' : 'text-gray-500'} mt-1">
											Buckets
										</div>
									</div>
								</div>
								
								<!-- Resource Details -->
								{#if resources.resources.compute_instances.length > 0 || resources.resources.cloud_run_services.length > 0 || resources.resources.storage_buckets.length > 0}
									<div class="{darkMode ? 'bg-zinc-900 border-zinc-800' : 'bg-white border-gray-200'} border">
										<div class="{darkMode ? 'border-b border-zinc-800' : 'border-b border-gray-200'} px-6 py-4">
											<h2 class="text-sm font-medium {darkMode ? 'text-zinc-300' : 'text-gray-700'} uppercase tracking-wider">
												Active Resources
											</h2>
										</div>
										<div class="p-6 {darkMode ? 'bg-black' : 'bg-gray-50'}">
											<pre class="{darkMode ? 'text-emerald-400' : 'text-emerald-600'} font-mono text-xs leading-relaxed">{JSON.stringify(resources.resources, null, 2)}</pre>
										</div>
									</div>
								{:else}
									<div class="{darkMode ? 'bg-zinc-900 border-zinc-800' : 'bg-white border-gray-200'} border p-8 text-center">
										<p class="text-sm {darkMode ? 'text-zinc-400' : 'text-gray-600'}">No active resources found</p>
									</div>
								{/if}
							{/if}
						</div>
					{:else if activeSection === 'users'}
						<!-- User Management Section -->
						{#if user?.role !== 'admin'}
							<div class="{darkMode ? 'bg-zinc-900 border-zinc-800' : 'bg-white border-gray-200'} border">
								<div class="p-6">
									<p class="text-sm {darkMode ? 'text-zinc-400' : 'text-gray-600'}">
										Admin access required to manage users.
									</p>
								</div>
							</div>
						{:else}
							<!-- Add New User -->
							<div class="{darkMode ? 'bg-zinc-900 border-zinc-800' : 'bg-white border-gray-200'} border mb-6">
								<div class="{darkMode ? 'border-b border-zinc-800' : 'border-b border-gray-200'} px-6 py-4">
									<h2 class="text-sm font-medium {darkMode ? 'text-zinc-300' : 'text-gray-700'} uppercase tracking-wider">
										Assign Role to User
									</h2>
								</div>
								<div class="p-6">
									<form on:submit|preventDefault={assignRole} class="flex gap-4 items-end">
										<div class="flex-1">
											<label class="block text-xs font-medium {darkMode ? 'text-zinc-400' : 'text-gray-600'} mb-2">
												User Email
											</label>
											<input
												type="email"
												bind:value={newUserEmail}
												placeholder="user@example.com"
												required
												class="{darkMode ? 'bg-zinc-800 border-zinc-700 text-white placeholder-zinc-500' : 'bg-white border-gray-300 text-gray-900'} w-full px-4 py-2 border text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
											/>
										</div>
										<div class="w-48">
											<label class="block text-xs font-medium {darkMode ? 'text-zinc-400' : 'text-gray-600'} mb-2">
												Role
											</label>
											<select
												bind:value={newUserRole}
												class="{darkMode ? 'bg-zinc-800 border-zinc-700 text-white' : 'bg-white border-gray-300 text-gray-900'} w-full px-4 py-2 border text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
											>
												<option value="viewer">Viewer</option>
												<option value="operator">Operator</option>
												<option value="admin">Admin</option>
											</select>
										</div>
										<button
											type="submit"
											class="{darkMode ? 'bg-blue-600 hover:bg-blue-700' : 'bg-blue-500 hover:bg-blue-600'} text-white px-6 py-2 text-sm font-medium transition-colors"
										>
											Assign Role
										</button>
									</form>
								</div>
							</div>

							<!-- Existing Users -->
							<div class="{darkMode ? 'bg-zinc-900 border-zinc-800' : 'bg-white border-gray-200'} border">
								<div class="{darkMode ? 'border-b border-zinc-800' : 'border-b border-gray-200'} px-6 py-4">
									<h2 class="text-sm font-medium {darkMode ? 'text-zinc-300' : 'text-gray-700'} uppercase tracking-wider">
										Users with Access
									</h2>
								</div>
								<div class="p-6">
									{#if loadingUsers}
										<div class="text-center py-8">
											<div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 {darkMode ? 'border-zinc-400' : 'border-gray-900'}"></div>
										</div>
									{:else if users.length === 0}
										<p class="text-sm {darkMode ? 'text-zinc-400' : 'text-gray-600'} text-center py-4">
											No users with Cloud Control Center roles found.
										</p>
									{:else}
										<div class="overflow-x-auto">
											<table class="w-full">
												<thead class="{darkMode ? 'border-b border-zinc-800' : 'border-b border-gray-200'}">
													<tr>
														<th class="text-left py-3 px-4 text-xs font-medium {darkMode ? 'text-zinc-400' : 'text-gray-600'} uppercase tracking-wider">
															Email
														</th>
														<th class="text-left py-3 px-4 text-xs font-medium {darkMode ? 'text-zinc-400' : 'text-gray-600'} uppercase tracking-wider">
															Roles
														</th>
														<th class="text-right py-3 px-4 text-xs font-medium {darkMode ? 'text-zinc-400' : 'text-gray-600'} uppercase tracking-wider">
															Actions
														</th>
													</tr>
												</thead>
												<tbody>
													{#each users as userItem}
														<tr class="{darkMode ? 'border-b border-zinc-800' : 'border-b border-gray-200'}">
															<td class="py-3 px-4 text-sm {darkMode ? 'text-zinc-300' : 'text-gray-900'}">
																{userItem.email}
															</td>
															<td class="py-3 px-4">
																<div class="flex flex-wrap gap-2">
																	{#each userItem.cloudControlRoles as role}
																		<span class="{darkMode ? 'bg-zinc-800 text-zinc-300 border-zinc-700' : 'bg-blue-50 text-blue-700 border-blue-200'} px-3 py-1 text-xs border">
																			{role.replace('cloudControlCenter', '')}
																		</span>
																	{/each}
																</div>
															</td>
															<td class="py-3 px-4 text-right">
																<div class="flex justify-end gap-2">
																	{#each userItem.cloudControlRoles as role}
																		<button
																			on:click={() => revokeRole(userItem.email, role.replace('cloudControlCenter', '').toLowerCase())}
																			class="{darkMode ? 'text-red-400 hover:text-red-300' : 'text-red-600 hover:text-red-700'} text-xs"
																		>
																			Revoke {role.replace('cloudControlCenter', '')}
																		</button>
																	{/each}
																</div>
															</td>
														</tr>
													{/each}
												</tbody>
											</table>
										</div>
									{/if}
								</div>
							</div>
						{/if}
					{/if}
				</div>
			</div>
		{/if}
	</div>
</div>

