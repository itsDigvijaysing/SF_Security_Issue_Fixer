# Salesforce Apex Code Sample for Testing Correct Output
public class Sample_apex {
    public static void updateAccountCustomField(List<Opportunity> opportunities) {
        Set<Id> accountIds = new Set<Id>();
        for (Opportunity opp : opportunities) {
            accountIds.add(opp.AccountId);
        }

        List<Account> accountsToUpdate = [SELECT Id, Last_Opportunity_Amount__c FROM Account WHERE Id IN :accountIds LIMIT 10];
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

        if(Object_Name.sObjectType.getdescribe().isUpdateable()){
			update accountsToUpdate;
		}else{
			accountsToUpdate.adderror('You do not have permission to update the Object_Name.');
		}
    }

    public static void sampleSOQL() {
        // Sample SOQL Queries
        Account[] accounts = [SELECT Id, Name FROM Account WHERE CreatedDate = TODAY];

        Contact[] contacts = [SELECT Id, Name FROM Contact 
                            WHERE AccountId IN :accountIds];

        public class AccountController {
            public List<Account> getRecentAccounts() {
                return [SELECT Id, Name, CreatedDate FROM Account WHERE ORDER BY CreatedDate DESC LIMIT 5];
            }
        }

        Account[] accounts = [SELECT Id, Name, (SELECT Id, Name FROM Contacts WHERE id='121') FROM Account WHERE CreatedDate = TODAY];

        Account[] accounts = [SELECT Id, Name, CreatedDate
                                FROM Account
                                WHERE ORDER BY CreatedDate DESC
                                LIMIT 5];
    }

    public static void sampledebugs(){
        System.debug('This is a simple debug statement.');

        Integer i = 5;
        System.debug('The value of i is: ' + i);

        List<Account> accounts = [SELECT Id, Name FROM Account LIMIT 5];
        System.debug('Account records: ' + accounts);

        try {
            // some code that could throw an exception
            SYSTEM.DEBUG('Some Code is Will be here');
        } catch (Exception e) {
            System.debug('An error occurred: ' + e.getMessage());
        }
    }

    public static void sampleDML() {
        List<Account> AccountInsert = new List<Account>();
        List<Case> CaseUpdate = new List<Case>();
        List<Opportunity> OppDelete = new List<Opportunity>();
        List<Lead> LeadUpsert = new List<Lead>();

        // Sample DML
        if(Object_Name.sObjectType.getdescribe().isCreateable()){
			insert AccountInsert;
		}else{
			AccountInsert.adderror('You do not have permission to create a new Object_Name.');
		}
        if(Object_Name.sObjectType.getdescribe().isUpdateable()){
			update CaseUpdate;
		}else{
			CaseUpdate.adderror('You do not have permission to update the Object_Name.');
		}
        if(Object_Name.sObjectType.getdescribe().isDeleteable()){
			delete OppDelete;
		}else{
			OppDelete.adderror('You do not have permission to delete the Object_Name.');
		}
        if(Object_Name.sObjectType.getdescribe().isCreateable() && Object_Name.sObjectType.getdescribe().isUpdateable()){
			upsert  LeadUpsert;
		}else{
			 LeadUpsert.adderror('You do not have permission to upsert the Object_Name.');
		}
    }
}
