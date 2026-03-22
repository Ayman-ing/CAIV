/**
 * Form Validation Composable
 * Provides consistent validation rules matching backend constraints
 */

import { ref, computed } from 'vue'

export interface ValidationRule {
  minLength?: number
  maxLength?: number
  minValue?: number
  maxValue?: number
  required?: boolean
  pattern?: RegExp
  custom?: (value: any) => string | null
}

export interface ValidationErrors {
  [field: string]: string | null
}

export const useFormValidation = () => {
  const errors = ref<ValidationErrors>({})

  /**
   * Validate string length
   */
  const validateLength = (
    value: string,
    minLength?: number,
    maxLength?: number
  ): string | null => {
    if (!value) return null

    const len = value.trim().length
    if (minLength && len < minLength) {
      return `Must be at least ${minLength} character${minLength !== 1 ? 's' : ''}`
    }
    if (maxLength && len > maxLength) {
      return `Must be no more than ${maxLength} character${maxLength !== 1 ? 's' : ''}`
    }
    return null
  }

  /**
   * Validate number range
   */
  const validateRange = (
    value: number | string,
    minValue?: number,
    maxValue?: number
  ): string | null => {
    if (value === '' || value === null) return null

    const num = typeof value === 'string' ? parseFloat(value) : value
    if (isNaN(num)) return 'Must be a valid number'

    if (minValue !== undefined && num < minValue) {
      return `Must be at least ${minValue}`
    }
    if (maxValue !== undefined && num > maxValue) {
      return `Must be no more than ${maxValue}`
    }
    return null
  }

  /**
   * Validate that end date is after start date
   */
  const validateEndDate = (endDate: string, startDate: string): string | null => {
    if (!endDate || !startDate) return null

    const end = new Date(endDate)
    const start = new Date(startDate)

    if (end < start) {
      return 'End date must be after start date'
    }
    return null
  }

  /**
   * Validate required field (not empty/whitespace)
   */
  const validateRequired = (value: string | any): string | null => {
    if (value === null || value === undefined) {
      return 'This field is required'
    }
    if (typeof value === 'string' && !value.trim()) {
      return 'This field cannot be empty'
    }
    return null
  }

  /**
   * Validate a field against rules
   */
  const validateField = (
    fieldName: string,
    value: any,
    rules: ValidationRule
  ): string | null => {
    // Custom validation first
    if (rules.custom) {
      const customError = rules.custom(value)
      if (customError) return customError
    }

    // Required check
    if (rules.required) {
      const requiredError = validateRequired(value)
      if (requiredError) return requiredError
    }

    // String validations
    if (typeof value === 'string') {
      if (rules.minLength || rules.maxLength) {
        const lengthError = validateLength(value, rules.minLength, rules.maxLength)
        if (lengthError) return lengthError
      }

      if (rules.pattern) {
        if (!rules.pattern.test(value)) {
          return `Invalid format for ${fieldName}`
        }
      }
    }

    // Number validations
    if (typeof value === 'number' || typeof value === 'string') {
      const numError = validateRange(
        value,
        rules.minValue,
        rules.maxValue
      )
      if (numError) return numError
    }

    return null
  }

  /**
   * Set error for a field
   */
  const setError = (fieldName: string, error: string | null) => {
    errors.value[fieldName] = error
  }

  /**
   * Clear error for a field
   */
  const clearError = (fieldName: string) => {
    errors.value[fieldName] = null
  }

  /**
   * Clear all errors
   */
  const clearErrors = () => {
    errors.value = {}
  }

  /**
   * Check if there are any errors
   */
  const hasErrors = computed(() => {
    return Object.values(errors.value).some(error => error !== null)
  })

  return {
    errors,
    validateLength,
    validateRange,
    validateEndDate,
    validateRequired,
    validateField,
    setError,
    clearError,
    clearErrors,
    hasErrors
  }
}
