<template>
  <div class="min-h-screen bg-background text-text flex">
    <aside class="w-64 bg-slate-900 border-r border-slate-800 hidden md:flex flex-col p-6 fixed h-full">
      <div class="text-2xl font-bold text-emerald-500 mb-10 tracking-tight">
        Intuitive<span class="text-white">Care</span>
      </div>
      <nav class="space-y-2">
        <router-link to="/" class="block px-4 py-2 rounded-lg hover:bg-slate-800 text-slate-300 hover:text-white transition" active-class="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          Dashboard
        </router-link>
        <router-link to="/operadoras" class="block px-4 py-2 rounded-lg hover:bg-slate-800 text-slate-300 hover:text-white transition" active-class="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          Operadoras
        </router-link>
      </nav>
    </aside>

    <main class="md:ml-64 flex-1 p-8 overflow-y-auto">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>