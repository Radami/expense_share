import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
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
    render(
      <BrowserRouter>
        <Group group={mockGroup} />
      </BrowserRouter>
    );
    expect(screen.getByText('Test Group')).toBeInTheDocument();
  });
}); 