// ✅ First: Place this mock at the very top
vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom');
  
    return {
      ...actual,
      useParams: () => ({ group_id: '1' }),
    };
  });

import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { type Mock, vi } from 'vitest';
import api from '../utils/axios';
import GroupDetailPage from './GroupDetailsPage';




// 1. Mock Child Components to isolate the GroupDetailsPage
vi.mock('./GroupDetailsExpenses', () => ({
  default: () => <div>Mocked Expenses Content</div>
}));
vi.mock('./GroupDetailsMembers', () => ({
  default: () => <div>Mocked Members Content</div>
}));
vi.mock('./GroupDetailsTotals', () => ({
  default: () => <div>Mocked Totals Content</div>
}));
vi.mock('./GroupDetailsBalances', () => ({
  default: () => <div>Mocked Balances Content</div>
}));

// 2. Mock API and Router Hooks
vi.mock('../utils/axios');



describe('GroupDetailPage component', () => {
    const mockApi = api.get as Mock;

    // Test data
    const mockGroupDetails = {
        name: 'Summer Trip',
        groupDescription: 'Planning for our summer trip.',
        expenses: [],
        group_members: [],
        totals: {},
        balances: {},
    };

    // Reset mocks before each test to ensure they are clean
    beforeEach(() => {      // useNavigate: () => vi.fn(), // Removed to allow real navigation
        vi.clearAllMocks();
    });

    // Helper function to render the component within a router
    const renderComponent = () => {
        render(
            <MemoryRouter initialEntries={['/group/1']}>
                <Routes>
                    <Route path="/group/:group_id" element={<GroupDetailPage />} />
                    <Route path="/add_expense/:group_id" element={<div>Navigated to Add Expense</div>} />
                </Routes>
            </MemoryRouter>
        );
    };

    describe('when data is fetched successfully', () => {
        beforeEach(() => {
            // Setup a successful API response for this block of tests
            mockApi.mockResolvedValue({ data: mockGroupDetails });
        });

        it('renders group name and tabs', async () => {
            renderComponent();
            await waitFor(() => {
                expect(screen.getByText('Summer Trip')).toBeInTheDocument();
            });

            // Check that all tabs are rendered
            expect(screen.getByRole('tab', { name: 'Expenses' })).toBeInTheDocument();
            expect(screen.getByRole('tab', { name: 'Members' })).toBeInTheDocument();
            expect(screen.getByRole('tab', { name: 'Totals' })).toBeInTheDocument();
            expect(screen.getByRole('tab', { name: 'Balances' })).toBeInTheDocument();
        });

        it('shows expenses content by default', async () => {
            renderComponent();
            await waitFor(() => {
                expect(screen.getByText('Mocked Expenses Content')).toBeInTheDocument();
            });

            expect(screen.getByRole('tab', { name: 'Expenses' })).toHaveClass('active');
            expect(screen.getByRole('tab', { name: 'Totals' })).not.toHaveClass('active');
            expect(screen.getByRole('tab', { name: 'Balances' })).not.toHaveClass('active');
            expect(screen.getByRole('tab', { name: 'Members' })).not.toHaveClass('active');
        });

        it('navigates to the add expense page when the button is clicked', async () => {
            renderComponent();
            await waitFor(() => {
                expect(screen.getByText('Summer Trip')).toBeInTheDocument();
            });

            const addExpenseButton = screen.getByRole('button', { name: /Add Expense/i });
            fireEvent.click(addExpenseButton);

            await waitFor(() => {
                expect(screen.getByText('Navigated to Add Expense')).toBeInTheDocument();
            });
        });

        it('switches to the members tab and displays its content on click', async () => {
            renderComponent();
            await waitFor(() => {
                expect(screen.getByText('Summer Trip')).toBeInTheDocument();
            });

            const membersTab = screen.getByRole('tab', { name: 'Members' });
            fireEvent.click(membersTab);
            
            await waitFor(() => {
                expect(screen.getByText('Mocked Members Content')).toBeInTheDocument();
            });

            // Check that the 'Members' tab is now the active one
            expect(membersTab).toHaveClass('active');
            expect(screen.getByRole('tab', { name: 'Totals' })).not.toHaveClass('active');
            expect(screen.getByRole('tab', { name: 'Balances' })).not.toHaveClass('active');
            expect(screen.getByRole('tab', { name: 'Expenses' })).not.toHaveClass('active');
        });

        it('switched to the totals tab and displays its content on clock', async() =>{
            renderComponent();
            await waitFor(() => {
                expect(screen.getByText('Summer Trip')).toBeInTheDocument();
            });

            const totalsTab = screen.getByRole('tab', {name: 'Totals'});
            fireEvent.click(totalsTab);

            expect(totalsTab).toHaveClass('active');
            expect(screen.getByRole('tab', { name: 'Expenses' })).not.toHaveClass('active');
            expect(screen.getByRole('tab', { name: 'Members' })).not.toHaveClass('active');
            expect(screen.getByRole('tab', { name: 'Balances' })).not.toHaveClass('active');
        });
    });

    describe('during loading and error states', () => {
        it('shows a loading/login message initially', () => {
            // Mock an API call that never resolves to simulate a loading state
            mockApi.mockReturnValue(new Promise(() => {})); 
            renderComponent();
            expect(screen.getByText('Please log in')).toBeInTheDocument();
            expect(screen.queryByText('Summer Trip')).not.toBeInTheDocument();
        });

        it('shows an error message if the API call fails', async () => {
            // Mock a rejected API call
            mockApi.mockRejectedValue(new Error('API Error'));
            renderComponent();
            await waitFor(() => {
                 expect(screen.getByText('Please log in')).toBeInTheDocument();
            });
            
            // The main content should not be rendered
            expect(screen.queryByText('Summer Trip')).not.toBeInTheDocument();
        });
    });
}); 