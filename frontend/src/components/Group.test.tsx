import { fireEvent, render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import type { GroupType } from '../../src/Types';
import Group from './Group';

describe('Group component', () => {
  const mockGroup: GroupType = {
    id: '1',
    name: 'Test Group',
    description: 'Test Description',
    creation_date: '2024-01-01',
    group_members: [],
    expenses: [],
    totals: {},
    balances: {},
    minimized_balances: [],
    minimize_balances_setting: false,
    user_is_owed: 'Nothing',
    user_owes: 'Nothing',
  };

  it('renders the group name', () => {
    const deleteGroup = vi.fn();
    render(
      <BrowserRouter>
        <Group group={mockGroup} deleteGroup={deleteGroup} />
      </BrowserRouter>
    );
    expect(screen.getByText('Test Group')).toBeInTheDocument();
  });

  it('calls the delete function when the delete button is clicked', () => {
    const deleteGroup = vi.fn();
    render(
      <BrowserRouter>
        <Group group={mockGroup} deleteGroup={deleteGroup} />
      </BrowserRouter>
    );

    const deleteButton = screen.getByRole('button', { name: /Group/i });
    fireEvent.click(deleteButton);
    expect(deleteGroup).toHaveBeenCalledWith(mockGroup.id);
  });
}); 