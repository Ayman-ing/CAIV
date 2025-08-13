<template>
  <div class="min-h-screen bg-background p-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-4xl font-bold text-text-primary mb-8">
        AI Resume Builder - UI Components
      </h1>
      
      <!-- Theme Toggle -->
      <div class="mb-8">
        <DarkModeToggle />
      </div>
      
      <!-- Buttons Section -->
      <Card title="Buttons" subtitle="Different button variants and sizes" class="mb-8">
        <div class="space-y-4">
          <div class="flex gap-4 flex-wrap">
            <Button variant="primary">Primary</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="destructive">Destructive</Button>
          </div>
          
          <div class="flex gap-4 flex-wrap items-center">
            <Button size="sm">Small</Button>
            <Button size="md">Medium</Button>
            <Button size="lg">Large</Button>
            <Button size="xl">Extra Large</Button>
          </div>
          
          <div class="flex gap-4 flex-wrap">
            <Button icon="lucide:plus" icon-position="left">Add Item</Button>
            <Button icon="lucide:download" icon-position="right">Download</Button>
            <Button :loading="isLoading" @click="toggleLoading">
              {{ isLoading ? 'Loading...' : 'Click to Load' }}
            </Button>
            <Button disabled>Disabled</Button>
          </div>
        </div>
      </Card>
      
      <!-- Forms Section -->
      <Card title="Form Components" subtitle="Input fields and form elements" class="mb-8">
        <div class="space-y-6 max-w-md">
          <Input
            v-model="form.email"
            label="Email Address"
            type="email"
            placeholder="Enter your email"
            left-icon="lucide:mail"
            required
          />
          
          <Input
            v-model="form.password"
            label="Password"
            type="password"
            placeholder="Enter your password"
            left-icon="lucide:lock"
            :error="passwordError"
            required
          />
          
          <Input
            v-model="form.search"
            label="Search"
            type="search"
            placeholder="Search for anything..."
            left-icon="lucide:search"
            hint="Try searching for 'developer' or 'designer'"
          />
          
          <Button variant="primary" block @click="submitForm">
            Submit Form
          </Button>
        </div>
      </Card>
      
      <!-- Modal Section -->
      <Card title="Modal Component" subtitle="Dialog and modal examples" class="mb-8">
        <div class="space-y-4">
          <div class="flex gap-4 flex-wrap">
            <Button @click="showModal = true">Open Modal</Button>
            <Button @click="showLargeModal = true" variant="outline">Large Modal</Button>
          </div>
        </div>
      </Card>
      
      <!-- Cards Section -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card variant="default" hover title="Default Card" subtitle="With hover effect">
          <p class="text-text-secondary">
            This is a default card with hover effect. Click me!
          </p>
        </Card>
        
        <Card variant="outline" title="Outline Card">
          <p class="text-text-secondary">
            This is an outline card variant.
          </p>
        </Card>
        
        <Card variant="ghost" shadow="none" title="Ghost Card">
          <p class="text-text-secondary">
            This is a ghost card with no shadow.
          </p>
        </Card>
      </div>
    </div>
    
    <!-- Modals -->
    <Modal v-model="showModal" title="Example Modal">
      <p class="mb-4">This is a simple modal example.</p>
      <p class="text-text-secondary">You can put any content here!</p>
      
      <template #footer>
        <Button variant="outline" @click="showModal = false">Cancel</Button>
        <Button variant="primary" @click="showModal = false">Confirm</Button>
      </template>
    </Modal>
    
    <Modal v-model="showLargeModal" title="Large Modal" size="xl">
      <div class="space-y-4">
        <p>This is a larger modal with more content.</p>
        
        <Input
          v-model="modalForm.name"
          label="Full Name"
          placeholder="Enter your full name"
        />
        
        <Input
          v-model="modalForm.email"
          label="Email"
          type="email"
          placeholder="Enter your email"
        />
        
        <div class="grid grid-cols-2 gap-4">
          <Card title="Card in Modal">
            <p class="text-sm text-text-secondary dark:text-white">
              You can nest components inside modals.
            </p>
          </Card>
          
          <Card title="Another Card">
            <p class="text-sm text-text-secondary dark:text-white">
              Components work seamlessly together.
            </p>
          </Card>
        </div>
      </div>
      
      <template #footer>
        <Button variant="outline" @click="showLargeModal = false">Cancel</Button>
        <Button variant="primary" @click="saveLargeModal">Save Changes</Button>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
// Import our UI components
import { Button, Input, Card, Modal } from '~/components/ui'

// Reactive data
const isLoading = ref(false)
const showModal = ref(false)
const showLargeModal = ref(false)

const form = reactive({
  email: '',
  password: '',
  search: ''
})

const modalForm = reactive({
  name: '',
  email: ''
})

// Computed
const passwordError = computed(() => {
  if (form.password && form.password.length < 6) {
    return 'Password must be at least 6 characters'
  }
  return ''
})

// Methods
const toggleLoading = () => {
  isLoading.value = true
  setTimeout(() => {
    isLoading.value = false
  }, 2000)
}

const submitForm = () => {
  console.log('Form submitted:', form)
  // Handle form submission
}

const saveLargeModal = () => {
  console.log('Modal form:', modalForm)
  showLargeModal.value = false
}

// SEO
useHead({
  title: 'UI Components - AI Resume Builder',
  meta: [
    { name: 'description', content: 'Modern UI components for AI Resume Builder' }
  ]
})
</script>

<style scoped>
/* Additional custom styles if needed */
.space-y-4 > * + * {
  margin-top: 1rem;
}

.space-y-6 > * + * {
  margin-top: 1.5rem;
}
</style>
