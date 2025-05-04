export function formatDate(dateString) {
    if (!dateString) return ""
    return `${dateString.slice(6, 8)}.${dateString.slice(4, 6)}.${dateString.slice(0, 4)}`
}

export function setLoadingStatus(vm, status, text, result = true) {
    vm.isLoading = status
    vm.loadingText = text
    vm.loadingResult = result
}