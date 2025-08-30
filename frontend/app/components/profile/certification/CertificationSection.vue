<script setup lang="ts">
// filepath: frontend/app/components/profile/certification/CertificationSection.vue
import { ref, computed } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'
import type { Certificate, CertificationFormData, CertificationDisplay } from './types'
import { CERTIFICATION_PROVIDERS } from './types'

// Certifications Data
const certifications = ref<Certificate[]>([])
const isExpanded = ref(false)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingCertification = ref<Certificate | null>(null)

// Form state
const formData = ref<CertificationFormData>({
  name: '',
  issuer: '',
  issueDate: '',
  expirationDate: '',
  credentialId: '',
  credentialUrl: '',
  neverExpires: false
})

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openAddModal = () => {
  isEditing.value = false
  editingCertification.value = null
  formData.value = {
    name: '',
    issuer: '',
    issueDate: '',
    expirationDate: '',
    credentialId: '',
    credentialUrl: '',
    neverExpires: false
  }
  isModalOpen.value = true
}

const openEditModal = (certification: Certificate) => {
  isEditing.value = true
  editingCertification.value = certification
  formData.value = {
    name: certification.name,
    issuer: certification.issuer,
    issueDate: certification.issueDate,
    expirationDate: certification.expirationDate || '',
    credentialId: certification.credentialId || '',
    credentialUrl: certification.credentialUrl || '',
    neverExpires: !certification.expirationDate
  }
  isModalOpen.value = true
}

const handleSave = () => {
  if (isEditing.value && editingCertification.value) {
    // Update existing certification
    const index = certifications.value.findIndex(cert => cert.id === editingCertification.value!.id)
    if (index !== -1 && certifications.value[index]) {
      certifications.value[index] = {
        ...certifications.value[index],
        name: formData.value.name.trim(),
        issuer: formData.value.issuer.trim(),
        issueDate: formData.value.issueDate,
        expirationDate: formData.value.neverExpires ? undefined : formData.value.expirationDate,
        credentialId: formData.value.credentialId.trim() || undefined,
        credentialUrl: formData.value.credentialUrl.trim() || undefined
      }
    }
  } else {
    // Add new certification
    const newCertification: Certificate = {
      id: Date.now(),
      name: formData.value.name.trim(),
      issuer: formData.value.issuer.trim(),
      issueDate: formData.value.issueDate,
      expirationDate: formData.value.neverExpires ? undefined : formData.value.expirationDate,
      credentialId: formData.value.credentialId.trim() || undefined,
      credentialUrl: formData.value.credentialUrl.trim() || undefined,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
    certifications.value.push(newCertification)
  }
  
  closeModal()
}

const closeModal = () => {
  isModalOpen.value = false
  editingCertification.value = null
  formData.value = {
    name: '',
    issuer: '',
    issueDate: '',
    expirationDate: '',
    credentialId: '',
    credentialUrl: '',
    neverExpires: false
  }
}

const removeCertification = (id: number) => {
  const index = certifications.value.findIndex(cert => cert.id === id)
  if (index !== -1) {
    certifications.value.splice(index, 1)
  }
}

const isFormValid = computed(() => {
  return formData.value.name.trim() !== '' && 
         formData.value.issuer.trim() !== '' && 
         formData.value.issueDate !== '' &&
         (formData.value.neverExpires || formData.value.expirationDate !== '')
})

const hasCertifications = computed(() => {
  return certifications.value.length > 0
})

// Enhanced display data
const displayCertifications = computed((): CertificationDisplay[] => {
  return certifications.value.map(cert => {
    const issueDate = new Date(cert.issueDate)
    const expirationDate = cert.expirationDate ? new Date(cert.expirationDate) : null
    const now = new Date()
    
    const formatDate = (dateStr: string) => {
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    }
    
    const isExpired = expirationDate ? expirationDate < now : false
    const daysUntilExpiration = expirationDate ? Math.ceil((expirationDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)) : undefined
    const isExpiringSoon = daysUntilExpiration !== undefined && daysUntilExpiration > 0 && daysUntilExpiration <= 30
    
    let status: 'active' | 'expired' | 'expiring-soon' = 'active'
    if (isExpired) status = 'expired'
    else if (isExpiringSoon) status = 'expiring-soon'
    
    return {
      ...cert,
      displayIssueDate: formatDate(cert.issueDate),
      displayExpirationDate: cert.expirationDate ? formatDate(cert.expirationDate) : undefined,
      isExpired,
      isExpiringSoon,
      daysUntilExpiration,
      hasCredentialUrl: !!cert.credentialUrl,
      status
    } as CertificationDisplay
  }).sort((a, b) => new Date(b.issueDate).getTime() - new Date(a.issueDate).getTime())
})

const getStatusColor = (status: string) => {
  const colors = {
    'active': 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 border-green-200 dark:border-green-800',
    'expired': 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 border-red-200 dark:border-red-800',
    'expiring-soon': 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800'
  }
  return colors[status as keyof typeof colors] || colors.active
}

const getStatusLabel = (status: string) => {
  const labels = {
    'active': 'Active',
    'expired': 'Expired',
    'expiring-soon': 'Expires Soon'
  }
  return labels[status as keyof typeof labels] || 'Active'
}
</script>

<template>
  <CollapsibleSection
    title="Certifications"
    description="Your professional certifications and credentials"
    icon="mdi:certificate"
    icon-color="text-yellow-600 dark:text-yellow-400"
    icon-bg-color="bg-yellow-100 dark:bg-yellow-900/30"
    button-color="bg-yellow-600 dark:bg-yellow-500 hover:bg-yellow-700 dark:hover:bg-yellow-600"
    :is-expanded="isExpanded"
    :is-empty="!hasCertifications"
    empty-message="Add your certifications"
    add-button-text="Add Certification"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Display Mode -->
    <div v-if="hasCertifications" class="space-y-6">
      <!-- Summary Stats -->
      <div class="flex items-center justify-between p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <Icon name="mdi:certificate-outline" class="w-5 h-5 text-yellow-600 dark:text-yellow-400" />
            <div>
              <p class="text-sm font-medium text-yellow-700 dark:text-yellow-300">Total Certifications</p>
              <p class="text-xs text-yellow-600 dark:text-yellow-400">{{ certifications.length }} certification{{ certifications.length !== 1 ? 's' : '' }}</p>
            </div>
          </div>
        </div>
        
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-yellow-600 hover:bg-yellow-700 dark:bg-yellow-500 dark:hover:bg-yellow-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:plus" class="w-4 h-4 mr-2" />
          Add Certification
        </button>
      </div>

      <!-- Certifications List -->
      <div class="space-y-4">
        <div v-for="certification in displayCertifications" :key="certification.id" class="relative p-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <!-- Status Badge -->
          <div class="absolute top-4 right-4">
            <span :class="getStatusColor(certification.status)" class="px-2 py-1 text-xs font-medium border rounded-full">
              {{ getStatusLabel(certification.status) }}
            </span>
          </div>
          
          <!-- Certification Name & Issuer -->
          <div class="mb-4 pr-20">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-1">
              {{ certification.name }}
            </h3>
            <div class="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
              <Icon name="mdi:domain" class="w-4 h-4" />
              <span class="font-medium">{{ certification.issuer }}</span>
            </div>
          </div>
          
          <!-- Dates -->
          <div class="grid grid-cols-2 gap-4 mb-4 text-sm">
            <div class="flex items-center space-x-2 text-gray-500 dark:text-gray-400">
              <Icon name="mdi:calendar-check" class="w-4 h-4" />
              <div>
                <p class="text-xs text-gray-400 dark:text-gray-500">Issued</p>
                <p>{{ certification.displayIssueDate }}</p>
              </div>
            </div>
            
            <div v-if="certification.displayExpirationDate" class="flex items-center space-x-2 text-gray-500 dark:text-gray-400">
              <Icon name="mdi:calendar-clock" class="w-4 h-4" />
              <div>
                <p class="text-xs text-gray-400 dark:text-gray-500">
                  {{ certification.isExpired ? 'Expired' : 'Expires' }}
                </p>
                <p>{{ certification.displayExpirationDate }}</p>
              </div>
            </div>
            
            <div v-else class="flex items-center space-x-2 text-green-600 dark:text-green-400">
              <Icon name="mdi:infinity" class="w-4 h-4" />
              <div>
                <p class="text-xs">Never expires</p>
              </div>
            </div>
          </div>
          
          <!-- Credential Info -->
          <div v-if="certification.credentialId || certification.hasCredentialUrl" class="mb-4 space-y-2">
            <div v-if="certification.credentialId" class="flex items-center space-x-2 p-2 bg-gray-50 dark:bg-gray-700 rounded border border-gray-200 dark:border-gray-600">
              <Icon name="mdi:identifier" class="w-4 h-4 text-gray-400" />
              <span class="text-sm text-gray-700 dark:text-gray-300">ID: {{ certification.credentialId }}</span>
            </div>
            
            <div v-if="certification.hasCredentialUrl" class="flex items-center space-x-2 p-2 bg-gray-50 dark:bg-gray-700 rounded border border-gray-200 dark:border-gray-600">
              <Icon name="mdi:link" class="w-4 h-4 text-gray-400" />
              <a
                :href="certification.credentialUrl"
                target="_blank"
                rel="noopener noreferrer"
                class="text-sm text-yellow-600 dark:text-yellow-400 hover:underline truncate"
              >
                Verify Credential
              </a>
            </div>
          </div>
          
          <!-- Warning for expiring/expired -->
          <div v-if="certification.status !== 'active'" class="mb-4">
            <div v-if="certification.status === 'expiring-soon'" class="flex items-center space-x-2 p-2 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded">
              <Icon name="mdi:clock-alert" class="w-4 h-4 text-yellow-600 dark:text-yellow-400" />
              <span class="text-sm text-yellow-700 dark:text-yellow-300">
                Expires in {{ certification.daysUntilExpiration }} day{{ certification.daysUntilExpiration !== 1 ? 's' : '' }}
              </span>
            </div>
            
            <div v-else-if="certification.status === 'expired'" class="flex items-center space-x-2 p-2 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded">
              <Icon name="mdi:alert-circle" class="w-4 h-4 text-red-600 dark:text-red-400" />
              <span class="text-sm text-red-700 dark:text-red-300">
                This certification has expired
              </span>
            </div>
          </div>
          
          <!-- Actions -->
          <div class="flex items-center justify-end space-x-2 pt-4 border-t border-gray-200 dark:border-gray-700">
            <button
              @click="openEditModal(certification)"
              class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex items-center"
            >
              <Icon name="mdi:pencil" class="w-4 h-4 mr-1" />
              Edit
            </button>
            
            <button
              @click="removeCertification(certification.id!)"
              class="px-3 py-1.5 text-sm bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors flex items-center"
            >
              <Icon name="mdi:delete" class="w-4 h-4 mr-1" />
              Remove
            </button>
          </div>
        </div>
      </div>
    </div>
  </CollapsibleSection>

  <!-- Add/Edit Modal -->
  <Modal
    v-model="isModalOpen"
    :title="isEditing ? 'Edit Certification' : 'Add Certification'"
    size="xl"
    @close="closeModal"
  >
    <template #header>
      <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
        {{ isEditing ? 'Edit Certification' : 'Add Certification' }}
      </h2>
    </template>
    
    <div class="grid grid-cols-2 gap-6">
      <!-- Certification Name -->
      <div>
        <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Certification Name *
        </label>
        <input
          id="name"
          v-model="formData.name"
          type="text"
          placeholder="e.g. AWS Certified Solutions Architect"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Full name of the certification
        </p>
      </div>

      <!-- Issuing Organization -->
      <div>
        <label for="issuer" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Issuing Organization *
        </label>
        <select
          id="issuer"
          v-model="formData.issuer"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        >
          <option value="">Select provider</option>
          <option v-for="provider in CERTIFICATION_PROVIDERS" :key="provider" :value="provider">
            {{ provider }}
          </option>
        </select>
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Organization that issued the certification
        </p>
      </div>

      <!-- Issue Date -->
      <div>
        <label for="issueDate" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Issue Date *
        </label>
        <input
          id="issueDate"
          v-model="formData.issueDate"
          type="date"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          When was this certification issued?
        </p>
      </div>

      <!-- Expiration Date -->
      <div>
        <label for="expirationDate" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Expiration Date
        </label>
        <input
          id="expirationDate"
          v-model="formData.expirationDate"
          type="date"
          :disabled="formData.neverExpires"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
          :required="!formData.neverExpires"
        />
        <div class="mt-2">
          <label class="flex items-center">
            <input
              v-model="formData.neverExpires"
              type="checkbox"
              class="rounded border-gray-300 dark:border-gray-600 text-yellow-600 focus:ring-yellow-500 dark:bg-gray-700"
            />
            <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Never expires</span>
          </label>
        </div>
      </div>

      <!-- Credential ID -->
      <div>
        <label for="credentialId" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Credential ID (Optional)
        </label>
        <input
          id="credentialId"
          v-model="formData.credentialId"
          type="text"
          placeholder="e.g. ABC123456"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Unique identifier for this certification
        </p>
      </div>

      <!-- Credential URL -->
      <div>
        <label for="credentialUrl" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Credential URL (Optional)
        </label>
        <input
          id="credentialUrl"
          v-model="formData.credentialUrl"
          type="url"
          placeholder="https://verify.example.com/credential"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Link to verify this certification
        </p>
      </div>

      <!-- Guidelines -->
      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 col-span-2">
        <div class="flex items-start space-x-2">
          <Icon name="mdi:lightbulb-outline" class="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
          <div class="text-sm text-blue-700 dark:text-blue-300">
            <p class="font-medium mb-1">Certification Tips</p>
            <ul class="text-xs space-y-1 list-disc list-inside">
              <li>Only include certifications relevant to your target roles</li>
              <li>Keep expired certifications if they're still valuable</li>
              <li>Include credential IDs and verification links when available</li>
              <li>Order by relevance and recency</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <button
        @click="closeModal"
        class="px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors"
      >
        Cancel
      </button>
      
      <button
        @click="handleSave"
        :disabled="!isFormValid"
        class="px-4 py-2 bg-yellow-600 hover:bg-yellow-700 dark:bg-yellow-500 dark:hover:bg-yellow-600 text-white rounded-lg transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Icon name="mdi:content-save" class="w-4 h-4 mr-2" />
        {{ isEditing ? 'Update Certification' : 'Save Certification' }}
      </button>
    </template>
  </Modal>
</template>
