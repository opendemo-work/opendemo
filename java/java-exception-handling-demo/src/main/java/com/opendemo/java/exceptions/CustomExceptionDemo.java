package com.opendemo.java.exceptions;

public class CustomExceptionDemo {
    public static void main(String[] args) {
        System.out.println("=== 自定义异常演示 ===\n");

        BankAccount account = new BankAccount("123456", 1000.0);

        try {
            account.deposit(500.0);
            System.out.println("存款成功，余额: $" + account.getBalance());
        } catch (BankOperationException e) {
            System.out.println("操作失败: " + e.getMessage());
        }

        demonstrateCustomExceptions(account);
        demonstrateExceptionChaining();
    }

    private static void demonstrateCustomExceptions(BankAccount account) {
        System.out.println("\n1. 自定义异常使用演示:");

        try {
            account.withdraw(2000.0);
        } catch (InsufficientFundsException e) {
            System.out.println("取款失败 - " + e.getMessage());
            System.out.println("账户余额: $" + e.getCurrentBalance());
            System.out.println("尝试取款: $" + e.getWithdrawAmount());
        } catch (InvalidAmountException | AccountFrozenException e) {
            System.out.println("操作失败: " + e.getMessage());
        }

        try {
            account.deposit(-100.0);
        } catch (InvalidAmountException e) {
            System.out.println("存款失败 - " + e.getMessage());
            System.out.println("无效金额: $" + e.getAmount());
        } catch (AccountFrozenException e) {
            System.out.println("操作受限 - " + e.getMessage());
        }

        try {
            account.freezeAccount();
            account.withdraw(100.0);
        } catch (AccountFrozenException e) {
            System.out.println("操作受限 - " + e.getMessage());
        } catch (BankOperationException e) {
            System.out.println("操作失败: " + e.getMessage());
        }
    }

    private static void demonstrateExceptionChaining() {
        System.out.println("\n2. 异常链示例:");
        try {
            processDataFromFile("config.txt");
        } catch (DataProcessingException e) {
            System.out.println("数据处理失败: " + e.getMessage());
            if (e.getCause() != null) {
                System.out.println("根本原因: " + e.getCause().getMessage());
            }
            System.out.println("\n异常堆栈跟踪:");
            e.printStackTrace();
        }
    }

    private static void processDataFromFile(String filename) throws DataProcessingException {
        try {
            if (!filename.equals("valid.txt")) {
                throw new FileReadException("文件不存在: " + filename);
            }
            String data = "invalid_data_format";
            if (data.startsWith("invalid")) {
                throw new DataFormatException("数据格式错误: " + data);
            }
            processBusinessLogic(data);
        } catch (FileReadException | DataFormatException e) {
            throw new DataProcessingException("处理文件数据时发生错误", e);
        }
    }

    private static void processBusinessLogic(String data) throws BusinessLogicException {
        if (data == null || data.isEmpty()) {
            throw new BusinessLogicException("业务数据为空");
        }
        System.out.println("业务处理成功: " + data);
    }
}
