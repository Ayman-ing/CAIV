<template>
  <Card 
    :hover="true" 
    :clickable="true"
    class="group transition-all duration-200"
    @click="$emit('action')"
  >
    <div class="p-6 text-center">
      <!-- Icon -->
      <div class="mb-4 flex justify-center">
        <div :class="[
          'p-3 rounded-full transition-all duration-200',
          iconBgColor,
          'group-hover:scale-110'
        ]">
          <Icon :name="icon" :class="['text-2xl', iconColor]" />
        </div>
      </div>
      
      <!-- Content -->
      <h3 class="text-lg font-semibold text-text-primary dark:text-text-primary mb-2">
        {{ title }}
      </h3>
      
      <p class="text-text-secondary dark:text-text-secondary mb-4 text-sm">
        {{ description }}
      </p>
      
      <!-- Action Button -->
      <Button 
        :variant="buttonVariant"
        :size="buttonSize"
        class="w-full"
        @click.stop="$emit('action')"
      >
        {{ buttonText }}
      </Button>
    </div>
  </Card>
</template>

<script setup lang="ts">
interface QuickActionCardProps {
  icon: string
  title: string
  description: string
  buttonText: string
  buttonVariant?: 'primary' | 'secondary' | 'outline' | 'ghost'
  buttonSize?: 'sm' | 'md' | 'lg'
  iconColor?: string
  iconBgColor?: string
}

interface QuickActionCardEmits {
  (e: 'action'): void
}

const props = withDefaults(defineProps<QuickActionCardProps>(), {
  buttonVariant: 'primary',
  buttonSize: 'md',
  iconColor: 'text-primary-600',
  iconBgColor: 'bg-primary-100 dark:bg-primary-900/20'
})

defineEmits<QuickActionCardEmits>()
</script>
