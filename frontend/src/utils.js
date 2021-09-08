export function showForLender() {
  if (localStorage.getItem('role') === 'lender') {
    return true
  } else {
    return false
  }
}

export function showForBorrower() {
  if (localStorage.getItem('role') === 'borrower') {
    return true
  } else {
    return false
  }
}