# SoloWealth Testing Checklist

## 🧪 Complete Testing Guide

### Prerequisites
1. ✅ Kill any existing process on port 8000
2. ✅ Run `npm start`
3. ✅ App should open automatically
4. ✅ Open browser DevTools (F12) > Console tab

---

## TEST 1: Dashboard & Filters ✅

### Test Case 1.1: Dashboard Loads
- [ ] Dashboard displays with 6 stat cards
- [ ] Monthly Salary, Total Expenses, Remaining Balance, Savings Rate, Net Worth, Total Debts
- [ ] Status badge shows (Rich/Neutral/Poor)

### Test Case 1.2: Month Filter
- [ ] Month selector shows only months with data
- [ ] Select a different month
- [ ] "Total Expenses (Filtered)" label appears
- [ ] Stats recalculate for selected month
- [ ] Recent expenses table updates

### Test Case 1.3: Empty States
- [ ] Select a month with no data
- [ ] Shows "No expenses for selected month" with calendar-x icon

---

## TEST 2: Expenses CRUD ✅

### Test Case 2.1: CREATE Expense
1. [ ] Click "+ Add Expense" button
2. [ ] Modal opens with title "Add Expense"
3. [ ] Fill in:
   - Date: Today
   - Category: Food
   - Amount: 500
   - Notes: Lunch
4. [ ] Click Save
5. [ ] ✅ Modal closes
6. [ ] ✅ Green toast: "Expense Added!"
7. [ ] ✅ Table refreshes with new expense
8. [ ] ✅ Dashboard updates

### Test Case 2.2: EDIT Expense
1. [ ] Click Edit button (pencil icon) on an expense
2. [ ] Modal opens with title "Edit Expense"
3. [ ] Form pre-filled with existing data
4. [ ] Category dropdown shows correct selection
5. [ ] Change amount to 600
6. [ ] Click Save
7. [ ] ✅ Modal closes
8. [ ] ✅ Orange toast: "Updated!"
9. [ ] ✅ Table shows updated amount (600)
10. [ ] ✅ No console errors

### Test Case 2.3: DELETE Expense
1. [ ] Click Delete button (trash icon)
2. [ ] Custom confirmation modal appears
3. [ ] Click "Confirm Delete"
4. [ ] ✅ Modal closes
5. [ ] ✅ Toast: "Deleted!"
6. [ ] ✅ Expense removed from table

---

## TEST 3: Investments CRUD ✅

### Test Case 3.1: CREATE Investment
1. [ ] Go to Investments page
2. [ ] Click "+ Add Investment"
3. [ ] Fill in:
   - Date: Today
   - Type: Deposit
   - Amount: 10000
   - Description: Mutual Fund
4. [ ] Click Save
5. [ ] ✅ Toast: "Investment Added!"
6. [ ] ✅ Table updates
7. [ ] ✅ Stats cards update

### Test Case 3.2: EDIT Investment
1. [ ] Click Edit button on investment
2. [ ] Modal title: "Edit Investment"
3. [ ] Change amount to 15000
4. [ ] Change type to Withdrawal
5. [ ] Click Save
6. [ ] ✅ Toast: "Updated!"
7. [ ] ✅ Table shows 15000 and Withdrawal
8. [ ] ✅ No errors in console

### Test Case 3.3: DELETE Investment
1. [ ] Click Delete button
2. [ ] Confirm deletion
3. [ ] ✅ Investment removed

---

## TEST 4: Debts CRUD ✅

### Test Case 4.1: CREATE Debt
1. [ ] Go to Debts page
2. [ ] Click "+ Add Debt"
3. [ ] Fill in:
   - Name: Car Loan
   - Principal: 500000
   - Remaining: 450000
   - Interest Rate: 8.5
   - Monthly Payment: 15000
4. [ ] Click Save
5. [ ] ✅ Toast: "Debt Added!"
6. [ ] ✅ Table updates

### Test Case 4.2: EDIT Debt
1. [ ] Click Edit button
2. [ ] Modal title: "Edit Debt"
3. [ ] Change Remaining to 430000
4. [ ] Click Save
5. [ ] ✅ Toast: "Updated!"
6. [ ] ✅ Shows new remaining amount

### Test Case 4.3: DELETE Debt
1. [ ] Click Delete
2. [ ] Confirm
3. [ ] ✅ Debt removed

---

## TEST 5: Recurring Expenses ✅

### Test Case 5.1: ADD Recurring Expense
1. [ ] Go to Settings page
2. [ ] Scroll to "Recurring Monthly Expenses"
3. [ ] Click "+ Add Recurring Expense"
4. [ ] Fill in:
   - Category: Rent
   - Amount: 15000
   - Auto-Apply: ✓ Checked
5. [ ] Click Save
6. [ ] ✅ Toast: "Recurring Expense Added!"
7. [ ] ✅ Appears in table with "Auto" badge

### Test Case 5.2: APPLY Now (Manual)
1. [ ] Click "Apply Now" on a recurring expense
2. [ ] ✅ Toast: "Applied!"
3. [ ] Go to Expenses page
4. [ ] ✅ New expense appears with note "Recurring: [Category]"

### Test Case 5.3: AUTO-APPLY (Monthly)
1. [ ] Clear localStorage: Open DevTools > Application > Local Storage > Clear All
2. [ ] Refresh page
3. [ ] ✅ Toast: "Recurring Expenses Applied! X recurring expense(s) added"
4. [ ] Go to Expenses
5. [ ] ✅ Auto expenses dated 1st of current month
6. [ ] Refresh page again
7. [ ] ✅ No duplicate toast (already applied this month)

### Test Case 5.4: DELETE Recurring Expense
1. [ ] Click Delete on recurring expense
2. [ ] Custom confirmation appears
3. [ ] Confirm
4. [ ] ✅ Toast: "Deleted!"
5. [ ] ✅ Removed from table

---

## TEST 6: Error Cases 🚨

### Test Case 6.1: Network Error (Simulated)
1. [ ] Stop the backend (close terminal with Ctrl+C)
2. [ ] Try to add an expense
3. [ ] ✅ Red error toast: "Failed to save expense. Please try again."
4. [ ] ✅ Console shows error details
5. [ ] ✅ Modal stays open

### Test Case 6.2: Invalid Data
1. [ ] Try to save expense with empty amount
2. [ ] ✅ HTML5 validation prevents submission
3. [ ] Try negative amount
4. [ ] ✅ HTML5 min="0" prevents it

---

## TEST 7: Settings & Reports ✅

### Test Case 7.1: Update Configuration
1. [ ] Go to Settings
2. [ ] Change Monthly Salary to 120000
3. [ ] Click Save Configuration
4. [ ] ✅ Toast: "Configuration saved!"
5. [ ] Go to Dashboard
6. [ ] ✅ Monthly Salary shows 120000

### Test Case 7.2: View Reports
1. [ ] Go to Reports page
2. [ ] ✅ Table shows monthly breakdown
3. [ ] ✅ Savings rate calculated per month
4. [ ] ✅ Status badge for each month

### Test Case 7.3: Export Data
1. [ ] Click "Export Data" button
2. [ ] ✅ CSV file downloads
3. [ ] ✅ Opens in Excel/Sheets
4. [ ] ✅ Contains all expenses

---

## ✅ Success Criteria

All tests should:
- [ ] ✅ Modal opens/closes correctly
- [ ] ✅ Correct toast notifications appear
- [ ] ✅ Data updates in real-time
- [ ] ✅ No JavaScript errors in console
- [ ] ✅ No network errors (200 OK responses)
- [ ] ✅ Forms reset after submission
- [ ] ✅ Edit shows pre-filled data
- [ ] ✅ Delete uses custom confirmation

---

## 🐛 If Errors Occur

### Error: "Failed to save/update"
- Check browser console for details
- Verify backend is running (should see "Application startup complete")
- Check Network tab: Status should be 200, not 404/500

### Error: "TypeError: Cannot read..."
- Check if data is loaded before accessing
- Verify all IDs match between HTML and JavaScript

### Error: Modal doesn't close
- Check if `closeModal()` is called
- Verify modal ID matches
- Check for JavaScript errors preventing execution

---

## 📊 Final Validation

After all tests:
- [ ] Dashboard shows accurate calculations
- [ ] All three CRUD sections work (Expenses, Investments, Debts)
- [ ] Recurring expenses auto-apply correctly
- [ ] Filters work and show proper empty states
- [ ] No console errors
- [ ] All toasts display correctly
- [ ] Custom modals replace default dialogs

**Status:** ✅ PASS / ❌ FAIL

---

*Keep browser DevTools open during testing to catch any errors!*
