import { useCallback, useEffect, useState } from 'react';
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import { type BalancesType, type ExpenseType, type GroupMemberType, type MinimizedDebtType } from '../Types';
import api from '../utils/axios';
import GroupDetailsBalances from './GroupDetailsBalances';
import GroupDetailsExpenses from './GroupDetailsExpenses';
import GroupDetailsMembers from './GroupDetailsMembers';
import GroupDetailsTotals from './GroupDetailsTotals';

export default function GroupDetailPage() {
    const { group_id = "" } = useParams<string>();
    const [searchParams, setSearchParams] = useSearchParams();
    const activeTab = searchParams.get('tab') ?? 'expenses';
    const [isError, setIsError] = useState(false);
    const [groupName, setGroupName] = useState("");
    const [groupDescription, setGroupDescription] = useState("");
    const [userIsOwed, setUserIsOwed] = useState<string>("Nothing");
    const [userOwes, setUserOwes] = useState<string>("Nothing");
    const [groupExpenses, setGroupExpenses] = useState<ExpenseType[]>([]);
    const [groupMembers, setGroupMembers] = useState<GroupMemberType[]>([]);
    const [groupBalances, setGroupBalances] = useState<BalancesType>({});
    const [groupMinimizedBalances, setGroupMinimizedBalances] = useState<MinimizedDebtType[]>([]);
    const [groupMinimizeBalancesSetting, setGroupMinimizeBalancesSetting] = useState<boolean>(false);

    const [isLoading, setIsLoading] = useState(true);

    const navigate = useNavigate();

    const fetchGroupDetails = useCallback(async () => {
        try {
            const response = await api.get('/splittime/api/group_details', {
                params: { group_id },
            });
            setGroupName(response.data.name);
            setGroupDescription(response.data.description);
            setUserIsOwed(response.data.user_is_owed);
            setUserOwes(response.data.user_owes);
            setGroupExpenses(response.data.expenses);
            setGroupMembers(response.data.group_members);
            setGroupBalances(response.data.balances);
            setGroupMinimizedBalances(response.data.minimized_balances);
            setGroupMinimizeBalancesSetting(response.data.minimize_balances_setting);
        } catch (error) {
            console.error('Error fetching group details', error);
            setIsError(true);
        } finally {
            setIsLoading(false);
        }
    }, [group_id]);

    useEffect(() => {
        fetchGroupDetails();
    }, [fetchGroupDetails]);

    return (
        <div className="py-4">
            {isLoading ? (
                <div className="d-flex justify-content-center py-5">
                    <div className="spinner-border text-success" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </div>
                </div>
            ) : isError ? (
                <div className="text-center py-5 text-secondary">
                    <i className="bi bi-exclamation-circle display-4 d-block mb-3 opacity-50"></i>
                    <p className="fs-5 fw-medium mb-1">Something went wrong</p>
                    <small>Please try again later</small>
                </div>
            ) : (
                <>
                    <div className="mb-3">
                        <h1 className="fw-bold mb-1">{groupName}</h1>
                        {groupDescription && <p className="text-secondary small mb-2">{groupDescription}</p>}
                        <div className="d-flex align-items-center gap-2 mt-1">
                            {userIsOwed === "Nothing"
                                ? <span className="badge rounded-pill bg-body-secondary text-secondary fw-medium px-3 py-2">You are owed nothing</span>
                                : <span className="badge rounded-pill bg-success-subtle text-success-emphasis fw-semibold px-3 py-2">You are owed {userIsOwed}</span>
                            }
                            {userOwes === "Nothing"
                                ? <span className="badge rounded-pill bg-body-secondary text-secondary fw-medium px-3 py-2">You owe nothing</span>
                                : <span className="badge rounded-pill bg-danger-subtle text-danger-emphasis fw-semibold px-3 py-2">You owe {userOwes}</span>
                            }
                            <div className="d-flex gap-2 ms-auto">
                                <button className="btn btn-outline-secondary btn-sm d-flex align-items-center gap-2" type="button" onClick={() => navigate(`/edit_group/${group_id}?return_tab=${activeTab}`)}>
                                    <i className="bi bi-pencil-square"></i> Edit group
                                </button>
                                <button className="btn btn-add-member btn-sm d-flex align-items-center gap-2" type="button" onClick={() => navigate(`/add_member/${group_id}?return_tab=${activeTab}`)}>
                                    <i className="bi bi-person-plus"></i> Add member
                                </button>
                                <button className="btn btn-add-expense btn-sm d-flex align-items-center gap-2" type="button" onClick={() => navigate(`/add_expense/${group_id}?return_tab=${activeTab}`)}>
                                    <i className="bi bi-plus-lg"></i> Add expense
                                </button>
                            </div>
                        </div>
                    </div>

                    <Tabs
                        activeKey={activeTab}
                        onSelect={k => k && setSearchParams({ tab: k }, { replace: true })}
                        id="group-detail-tabs"
                        className="mb-3 custom-tab-margin gap-1"
                        variant="pills"
                    >
                        <Tab eventKey="expenses" title="Expenses">
                            <GroupDetailsExpenses group_expenses={groupExpenses} group_members={groupMembers} group_id={group_id} />
                        </Tab>
                        <Tab eventKey="members" title="Members">
                            <GroupDetailsMembers group_members={groupMembers} group_id={group_id} />
                        </Tab>
                        <Tab eventKey="totals" title="Totals">
                            <GroupDetailsTotals groupExpenses={groupExpenses} groupMembers={groupMembers} />
                        </Tab>
                        <Tab eventKey="balances" title="Balances">
                            <GroupDetailsBalances
                                group_balances={groupBalances}
                                group_minimized_balances={groupMinimizedBalances}
                                minimize_balances_setting={groupMinimizeBalancesSetting}
                                group_members={groupMembers}
                                group_id={group_id}
                                onRefresh={fetchGroupDetails}
                            />
                        </Tab>
                    </Tabs>
                </>
            )}
        </div>
    );
}