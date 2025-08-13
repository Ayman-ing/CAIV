<template>
  <Card title="Recent Activity" class="mb-8">
    <div v-if="activities.length === 0" class="text-center py-8">
      <Icon name="lucide:activity" class="text-4xl text-text-muted dark:text-text-muted mb-4" />
      <p class="text-text-muted dark:text-text-muted">No recent activity yet</p>
      <p class="text-sm text-text-muted dark:text-text-muted mt-2">Start creating your first resume to see activity here</p>
    </div>
    
    <div v-else class="space-y-4">
      <div 
        v-for="activity in activities" 
        :key="activity.id"
        class="flex items-center gap-4 p-3 hover:bg-surface-hover dark:hover:bg-surface-hover rounded-md transition-colors"
      >
        <!-- Activity Icon -->
        <div :class="[
          'p-2 rounded-full',
          getActivityIconBg(activity.type)
        ]">
          <Icon :name="getActivityIcon(activity.type)" :class="[
            'w-4 h-4',
            getActivityIconColor(activity.type)
          ]" />
        </div>
        
        <!-- Activity Details -->
        <div class="flex-1">
          <p class="text-sm font-medium text-text-primary dark:text-text-primary">
            {{ activity.title }}
          </p>
          <p class="text-xs text-text-muted dark:text-text-muted">
            {{ formatDate(activity.date) }}
          </p>
        </div>
        
        <!-- Action Button -->
        <Button 
          v-if="activity.actionText"
          variant="ghost" 
          size="sm"
          @click="$emit('activityAction', activity)"
        >
          {{ activity.actionText }}
        </Button>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
interface Activity {
  id: string
  type: 'create' | 'edit' | 'download' | 'share' | 'upload'
  title: string
  date: Date
  actionText?: string
}

interface RecentActivityProps {
  activities: Activity[]
}

interface RecentActivityEmits {
  (e: 'activityAction', activity: Activity): void
}

defineProps<RecentActivityProps>()
defineEmits<RecentActivityEmits>()

// Activity icon mapping
const getActivityIcon = (type: string) => {
  const icons = {
    create: 'lucide:plus',
    edit: 'lucide:edit',
    download: 'lucide:download',
    share: 'lucide:share',
    upload: 'lucide:upload'
  }
  return icons[type as keyof typeof icons] || 'lucide:activity'
}

const getActivityIconColor = (type: string) => {
  const colors = {
    create: 'text-green-600',
    edit: 'text-blue-600',
    download: 'text-purple-600',
    share: 'text-orange-600',
    upload: 'text-indigo-600'
  }
  return colors[type as keyof typeof colors] || 'text-gray-600'
}

const getActivityIconBg = (type: string) => {
  const backgrounds = {
    create: 'bg-green-100 dark:bg-green-900/20',
    edit: 'bg-blue-100 dark:bg-blue-900/20',
    download: 'bg-purple-100 dark:bg-purple-900/20',
    share: 'bg-orange-100 dark:bg-orange-900/20',
    upload: 'bg-indigo-100 dark:bg-indigo-900/20'
  }
  return backgrounds[type as keyof typeof backgrounds] || 'bg-gray-100 dark:bg-gray-900/20'
}

const formatDate = (date: Date) => {
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return 'Today'
  if (days === 1) return 'Yesterday'
  if (days < 7) return `${days} days ago`
  
  return date.toLocaleDateString()
}
</script>
