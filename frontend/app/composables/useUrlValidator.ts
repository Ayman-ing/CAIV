/**
 * URL Validation Composable
 * Provides URL validation matching backend HttpUrl validation
 */

export const useUrlValidator = () => {
  /**
   * Validates if a string is a valid HTTP/HTTPS URL
   * Matches Pydantic's HttpUrl validation
   */
  const isValidUrl = (url: string): boolean => {
    if (!url || url.trim() === '') {
      return true // Optional URLs are valid when empty
    }

    try {
      // Try to create a URL object - this will throw if invalid
      const urlObj = new URL(url)
      // Only allow http and https protocols
      return urlObj.protocol === 'http:' || urlObj.protocol === 'https:'
    } catch {
      return false
    }
  }

  /**
   * Get error message for invalid URL
   */
  const getUrlErrorMessage = (url: string): string | null => {
    if (!url || url.trim() === '') {
      return null // No error for empty URLs
    }

    if (!isValidUrl(url)) {
      return 'Please enter a valid URL starting with http:// or https://'
    }

    return null
  }

  /**
   * Normalize URL - add https:// if no protocol is provided
   */
  const normalizeUrl = (url: string): string => {
    if (!url || url.trim() === '') {
      return ''
    }

    const trimmed = url.trim()
    if (!trimmed.startsWith('http://') && !trimmed.startsWith('https://')) {
      return `https://${trimmed}`
    }

    return trimmed
  }

  return {
    isValidUrl,
    getUrlErrorMessage,
    normalizeUrl
  }
}
