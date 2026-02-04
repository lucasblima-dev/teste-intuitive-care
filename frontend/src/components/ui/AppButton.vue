<script setup lang="ts">
defineProps<{ variant?: 'primary' | 'outline' }>();
</script>

<template>
  <button
    class="px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
    :class="variant === 'outline' 
      ? 'border border-slate-600 text-slate-300 hover:border-primary hover:text-primary' 
      : 'bg-primary text-white hover:bg-primaryHover shadow-lg shadow-emerald-900/20'"
  >
    <slot />
  </button>
</template>