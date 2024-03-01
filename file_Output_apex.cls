# Salesforce Apex Code Sample for Testing Correct Output
public class Sample_apex {
    public static void updateAccountCustomField(List<Opportunity> opportunities) {
        Set<Id> accountIds = new Set<Id>();
        for (Opportunity opp : opportunities) {
            accountIds.add(opp.AccountId);
        }

        List<Account> accountsToUpdate = [SELECT Id, Last_Opportunity_Amount__c FROM Account WHERE Id IN :accountIds WITH USER_MODE LIMIT 10];
        Map<Id, Decimal> accountIdToAmountMap = new Map<Id, Decimal>();

        for (Opportunity opp : opportunities) {
            if (accountIdToAmountMap.containsKey(opp.AccountId)) {
                accountIdToAmountMap.put(opp.AccountId, accountIdToAmountMap.get(opp.AccountId) + opp.Amount);
            } else {
                accountIdToAmountMap.put(opp.AccountId, opp.Amount);
            }
        }

        for (Account acc : accountsToUpdate) {
            acc.Last_Opportunity_Amount__c = accountIdToAmountMap.get(acc.Id);
        }

        update accountsToUpdate;
    }

    public static void sampleSOQL() {
        // Sample SOQL Queries
        Account[] accounts = [SELECT Id, Name FROM Account WHERE CreatedDate = TODAY WITH USER_MODE ];

        Contact[] contacts = [SELECT Id, Name FROM Contact 
                            WHERE AccountId IN :accountIds WITH USER_MODE ];

        public class AccountController {
            public List<Account> getRecentAccounts() {
                return [SELECT Id, Name, CreatedDate FROM Account WHERE WITH USER_MODE ORDER BY CreatedDate DESC LIMIT 5];
            }
        }

        Account[] accounts = [SELECT Id, Name, (SELECT Id, Name FROM Contacts) FROM Account WHERE CreatedDate = TODAY WITH USER_MODE ];

        Account[] accounts = [SELECT Id, Name, CreatedDate
                                FROM Account
                                WHERE WITH USER_MODE ORDER BY CreatedDate DESC
                                LIMIT 5];

    }

    public static void sampleDML() {
        List<Account> AccountInsert = new List<Account>();
        List<Case> CaseUpdate = new List<Case>();
        List<Opportunity> OppDelete = new List<Opportunity>();
        List<Lead> LeadUpsert = new List<Lead>();

        // Sample DML
        insert AccountInsert;
        update CaseUpdate;
        delete OppDelete;
        upsert  LeadUpsert;
    }
}
