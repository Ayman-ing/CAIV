<script setup lang="ts">
// filepath: frontend/app/components/profile/certification/CertificationSection.vue
import { ref, computed, onMounted } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'
import type { Certificate, CertificationFormData, CertificationDisplay } from './types'
import { CERTIFICATION_PROVIDERS } from './types'
import { useProfileStore } from '~/stores/profileStore'
import { profileSectionsService } from '~/services/profileSectionsService'
import { useToast } from '~/composables/useToast'

const profileStore = useProfileStore()
const activeProfile = profileStore.activeProfile
const { success, error } = useToast()

// Certifications Data
const certifications = ref<Certificate[]>([])
const isExpanded = ref(false)
const isLoading = ref(false)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingCertification = ref<Certificate | null>(null)
const isDeleteModalOpen = ref(false)
const certificationToDelete = ref<Certificate | null>(null)
const isDeleting = ref(false)

// Form state
const formData = ref<CertificationFormData>({
  name: '',
  issuing_organization: '',
  issue_date: '',
  expiration_date: '',
  credential_id: '',
  neverExpires: false
})

onMounted(async () => {
  await fetchCertifications()
})

const fetchCertifications = async () => {
  if (!activeProfile.value?.uuid) return
  isLoading.value = true
  try {
    const data = await profileSectionsService.getAllCertifications(activeProfile.value.uuid)
    certifications.value = data
  } catch (error) {
    console.error('Failed to fetch certifications:', error)
  } finally {
    isLoading.value = false
  }
}

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openAddModal = () => {
  isEditing.value = false
  editingCertification.value = null
  formData.value = {
    name: '',
    issuing_organization: '',
    issue_date: '',
    expiration_date: '',
    credential_id: '',
    neverExpires: false
  }
  isModalOpen.value = true
}

const openEditModal = (cert: Certificate) => {
  isEditing.value = true
  editingCertification.value = cert
  formData.value = {
    name: cert.name,
    issuing_organization: cert.issuing_organization,
    issue_date: cert.issue_date,
    expiration_date: cert.expiration_date || '',
    credential_id: cert.credential_id || '',
    neverExpires: !cert.expiration_date
  }
  isModalOpen.value = true
}

const handleSave = async () => {
  if (!activeProfile.value?.uuid) return
  
  const payload: Omit<Certificate, 'uuid'> = {
    name: formData.value.name.trim(),
    issuing_organization: formData.value.issuing_organization.trim(),
    issue_date: formData.value.issue_date,
    expiration_date: formData.value.neverExpires ? null : formData.value.expiration_date,
    credential_id: formData.value.credential_id.trim() || null
  }

  try {
    if (isEditing.value && editingCertification.value) {
      await profileSectionsService.updateCertificate(
        activeProfile.value.uuid,
        editingCertification.value.uuid,
        payload
      )
      success('Certification updated successfully!')
    } else {
      await profileSectionsService.createCertificate(activeProfile.value.uuid, payload)
      success('Certification added successfully!')
    }
    await fetchCertifications()
    closeModal()
  } catch (err) {
    error(`Failed to save certification: ${err instanceof Error ? err.message : 'Unknown error'}`)
  }
}

const closeModal = () => {
  isModalOpen.value = false
  editingCertification.value = null
}

const openDeleteModal = (cert: Certificate) => {
  certificationToDelete.value = cert
  isDeleteModalOpen.value = true
}

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false
  certificationToDelete.value = null
}

const confirmDelete = async () => {
  if (!activeProfile.value?.uuid || !certificationToDelete.value) return
  isDeleting.value = true
  try {
    await profileSectionsService.deleteCertificate(activeProfile.value.uuid, certificationToDelete.value.uuid)
    await fetchCertifications()
    closeDeleteModal()
    success('Certification deleted successfully!')
  } catch (err) {
    error(`Failed to delete certification: ${err instanceof Error ? err.message : 'Unknown error'}`)
  } finally {
    isDeleting.value = false
  }
}

const isFormValid = computed(() => {
  return formData.value.name.trim() !== '' && 
         formData.value.issuing_organization.trim() !== '' && 
         formData.value.issue_date !== '' &&
         (formData.value.neverExpires || formData.value.expiration_date !== '')
})

const hasCertifications = computed(() => {
  return certifications.value.length > 0
})

// Enhanced display data
const displayCertifications = computed((): CertificationDisplay[] => {
  return certifications.value.map(cert => {
    const now = new Date()
    const formatDate = (dateStr: string) => {
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    }
    
    const expDate = cert.expiration_date ? new Date(cert.expiration_date) : null
    const isExpired = expDate ? expDate < now : false
    const daysUntilExpiration = expDate ? Math.ceil((expDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)) : undefined
    const isExpiringSoon = daysUntilExpiration !== undefined && daysUntilExpiration > 0 && daysUntilExpiration <= 30
    
    let status: 'active' | 'expired' | 'expiring-soon' = 'active'
    if (isExpired) status = 'expired'
    else if (isExpiringSoon) status = 'expiring-soon'
    
    return {
      ...cert,
      displayIssueDate: formatDate(cert.issue_date),
      displayExpirationDate: cert.expiration_date ? formatDate(cert.expiration_date) : undefined,
      isExpired,
      isExpiringSoon,
      daysUntilExpiration,
      status
    } as CertificationDisplay
  }).sort((a, b) => new Date(b.issue_date).getTime() - new Date(a.issue_date).getTime())
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
    :is-empty="!isLoading && certifications.length === 0"
    empty-message="Add your certifications"
    add-button-text="Add Certification"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center p-8 text-yellow-600">
      <Icon name="mdi:loading" class="w-8 h-8 animate-spin" />
    </div>

    <!-- Display Mode -->
    <div v-else-if="hasCertifications" class="space-y-6">
      <!-- Summary Stats -->
      <div class="flex items-center justify-between p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <Icon name="mdi:certificate" class="w-5 h-5 text-yellow-600 dark:text-yellow-400" />
            <div>
              <p class="text-sm font-medium text-yellow-700 dark:text-yellow-300">Certifications</p>
              <p class="text-xs text-yellow-600 dark:text-yellow-400">{{ displayCertifications.length }} certification{{ displayCertifications.length !== 1 ? 's' : '' }}</p>
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
      <div class="space-y-6">
        <div v-for="cert in displayCertifications" :key="cert.uuid" class="relative p-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md transition-shadow">
        <div class="absolute top-4 right-4 text-xs font-medium px-2 py-1 rounded-full border" :class="getStatusColor(cert.status)">
          {{ getStatusLabel(cert.status) }}
        </div>
        
        <div class="mb-4 pr-20">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-1">{{ cert.name }}</h3>
          <div class="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
            <Icon name="mdi:domain" class="w-4 h-4" />
            <span class="font-medium">{{ cert.issuing_organization }}</span>
          </div>
        </div>
        
        <div class="grid grid-cols-2 gap-4 mb-4 text-sm text-gray-500 dark:text-gray-400">
          <div class="flex items-center space-x-2">
            <Icon name="mdi:calendar-check" class="w-4 h-4" />
            <span>Issued: {{ cert.displayIssueDate }}</span>
          </div>
          <div class="flex items-center space-x-2" v-if="cert.displayExpirationDate">
            <Icon name="mdi:calendar-clock" class="w-4 h-4" />
            <span>Expires: {{ cert.displayExpirationDate }}</span>
          </div>
          <div class="flex items-center space-x-2 text-green-600 dark:text-green-400" v-else>
            <Icon name="mdi:infinity" class="w-4 h-4" />
            <span>Never expires</span>
          </div>
        </div>
        
        <div v-if="cert.credential_id" class="mb-4 text-sm bg-gray-50 dark:bg-gray-700 p-2 rounded">
          <span class="text-gray-500 mr-2">Credential ID:</span>
          <span class="font-mono">{{ cert.credential_id }}</span>
        </div>
        
        <!-- Actions -->
        <div class="flex items-center justify-end space-x-2 pt-4 border-t border-gray-200 dark:border-gray-700">
          <button
            @click="openEditModal(cert)"
            class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex items-center"
          >
            <Icon name="mdi:pencil" class="w-4 h-4 mr-1" />
            Edit
          </button>
          
          <button
            @click="openDeleteModal(cert)"
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
  <!-- Delete Confirmation Modal -->
  <Modal
    v-model="isDeleteModalOpen"
    title="Delete Certification"
    size="sm"
    @close="closeDeleteModal"
  >
    <div class="space-y-4">
      <div class="flex items-start space-x-4">
        <Icon name="mdi:alert-circle" class="w-6 h-6 text-red-600 dark:text-red-400 flex-shrink-0" />
        <div class="flex-grow">
          <p class="text-gray-900 dark:text-gray-100 font-medium">Delete Certification?</p>
          <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">
            Are you sure you want to delete <span class="font-semibold">{{ certificationToDelete?.name }}</span>? This action cannot be undone.
          </p>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end space-x-3">
        <button
          @click="closeDeleteModal"
          :disabled="isDeleting"
          class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Cancel
        </button>
        <button
          @click="confirmDelete"
          :disabled="isDeleting"
          class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isDeleting ? 'Deleting...' : 'Delete' }}
        </button>
      </div>
    </template>
  </Modal>
  <!-- Add/Edit Modal -->
  <Modal
    v-model="isModalOpen"
    :title="isEditing ? 'Edit Certification' : 'Add Certification'"
    size="xl"
    @close="closeModal"
  >
    <div class="grid grid-cols-2 gap-6">
      <div class="col-span-2">
        <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Certification Name *
        </label>
        <input
          id="name"
          v-model="formData.name"
          type="text"
          placeholder="e.g. AWS Certified Developer"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
      </div>

      <div class="col-span-2">
        <label for="issuer" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Issuing Organization *
        </label>
        <select
          id="issuer"
          v-model="formData.issuing_organization"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        >
          <option value="">Select provider</option>
          <option v-for="p in CERTIFICATION_PROVIDERS" :key="p" :value="p">{{ p }}</option>
        </select>
      </div>

      <div>
        <label for="issue_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Issue Date *
        </label>
        <input
          id="issue_date"
          v-model="formData.issue_date"
          type="date"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
      </div>

      <div>
        <label for="expiration_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Expiration Date
        </label>
        <input
          id="expiration_date"
          v-model="formData.expiration_date"
          type="date"
          :disabled="formData.neverExpires"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 disabled:opacity-50"
        />
        <div class="mt-2">
          <label class="flex items-center text-sm">
            <input v-model="formData.neverExpires" type="checkbox" class="rounded text-yellow-600 mr-2" />
            Never expires
          </label>
        </div>
      </div>

      <div class="col-span-2">
        <label for="credential_id" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Credential ID (Optional)
        </label>
        <input
          id="credential_id"
          v-model="formData.credential_id"
          type="text"
          placeholder="e.g. 12345ABC"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        />
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end space-x-3">
        <button
          @click="closeModal"
          class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          Cancel
        </button>
        <button
          @click="handleSave"
          :disabled="!isFormValid"
          class="px-4 py-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isEditing ? 'Update' : 'Save' }}
        </button>
      </div>
    </template>
  </Modal>
</template>
