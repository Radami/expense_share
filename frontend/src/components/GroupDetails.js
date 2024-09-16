import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import {
    useParams
} from "react-router-dom";
import GroupDetailsBalances from './GroupDetailsBalances';
import GroupDetailsExpenses from './GroupDetailsExpenses';
import GroupDetailsMembers from './GroupDetailsMembers';
import GroupDetailsTotals from './GroupDetailsTotals';

function GroupDetails({ loginParams}) {

    const { groupId } = useParams();

    return (
        <div className="container col-lg-4 mt-3 text-white">
            <span className="h1">{groupId} - </span><span className="h2">{groupId}</span>
            

            <Tabs
                defaultActiveKey="expenses"
                id="fill-tab-example"
                className="mb-3 custom-tab-margin"
                variant='pills'
            >
                <Tab eventKey="expenses" title="Expenses">
                    <GroupDetailsExpenses />
                </Tab>
                <Tab eventKey="mebmers" title="Members">
                    <GroupDetailsMembers />
                </Tab>
                <Tab eventKey="totals" title="Totals">
                    <GroupDetailsTotals />
                </Tab>
                <Tab eventKey="balances"  title="Balances">
                    <GroupDetailsBalances />
                </Tab>
            </Tabs>    
        </div>
    );
}

    export default GroupDetails;