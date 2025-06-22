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
  };

  it('renders the group name', () => {
    const delete_function = vi.fn();
    render(
      <BrowserRouter>
        <Group group={mockGroup} delete_function={delete_function} />
      </BrowserRouter>
    );
    expect(screen.getByText('Test Group')).toBeInTheDocument();
  });

  it('calls the delete function when the delete button is clicked', () => {
    const delete_function = vi.fn();
    render(
      <BrowserRouter>
        <Group group={mockGroup} delete_function={delete_function} />
      </BrowserRouter>
    );

    const deleteButton = screen.getByRole('button', { name: /Group/i });
    fireEvent.click(deleteButton);
    expect(delete_function).toHaveBeenCalledWith(mockGroup.id);
  });
}); 