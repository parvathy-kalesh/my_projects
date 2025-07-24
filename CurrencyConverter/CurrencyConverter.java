import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class CurrencyConverter extends JFrame implements ActionListener {

    private JComboBox<String> fromCurrency, toCurrency;
    private JTextField amountField;
    private JButton convertButton;
    private JLabel resultLabel;

    private String[] currencyNames = {
        "USD", "EUR", "INR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "NZD", "SEK", "MXN"
    };

    // Approximate static exchange rates matrix:
    // rates[from][to]
    private double[][] rates = {
        //USD,  EUR,  INR,  GBP,   JPY,  AUD,  CAD,  CHF,  CNY,  NZD,  SEK,  MXN
        {1.0,   0.91, 83.0, 0.78, 142.0, 1.47, 1.33, 0.92, 7.0,  1.52, 10.3, 17.0},   // USD
        {1.10,  1.0,  91.0, 0.86, 156.0, 1.62, 1.47, 1.01, 7.7,  1.68, 11.3, 18.6},   // EUR
        {0.012, 0.011,1.0,  0.0095,1.7,  0.018,0.016,0.011,0.085,0.018,0.12, 0.20},   // INR
        {1.28,  1.16, 105.0,1.0,  181.0, 1.89, 1.72, 1.18, 8.3,  2.0,  13.2, 21.8},   // GBP
        {0.0070,0.0064,0.59,0.0055,1.0,  0.010,0.0095,0.0064,0.046,0.011,0.073,0.12},  // JPY
        {0.68,  0.62, 56.0, 0.53,  98.0,  1.0,  0.91, 0.62, 4.8,  0.68, 7.0,  11.6},   // AUD
        {0.75,  0.68, 61.0, 0.58,  104.0, 1.1,  1.0,  0.68, 5.3,  0.75, 7.7,  12.8},   // CAD
        {1.09,  0.99, 90.0, 0.85,  156.0, 1.61, 1.47, 1.0,  7.8,  1.67, 11.3, 18.6},   // CHF
        {0.14,  0.13, 12.0, 0.12,  21.0,  0.21, 0.19, 0.13, 1.0,  0.21, 1.44, 2.37},   // CNY
        {0.66,  0.60, 54.0, 0.53,  94.0,  1.47, 1.33, 0.60, 4.7,  1.0,  6.5,  11.0},   // NZD
        {0.097, 0.088,8.0,  0.076,13.3,  0.14, 0.13, 0.088,1.0,  0.15, 1.0,  1.7},    // SEK
        {0.059, 0.054,4.9,  0.046,8.1,   0.08, 0.078,0.054,0.42, 0.091,0.59, 1.0}     // MXN
    };

    public CurrencyConverter() {
        setTitle("Currency Converter");
        setSize(450, 250);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLocationRelativeTo(null); // center window
        setLayout(new GridLayout(5, 2, 10, 10));

        add(new JLabel("From Currency:"));
        fromCurrency = new JComboBox<>(currencyNames);
        add(fromCurrency);

        add(new JLabel("To Currency:"));
        toCurrency = new JComboBox<>(currencyNames);
        add(toCurrency);

        add(new JLabel("Amount:"));
        amountField = new JTextField();
        add(amountField);

        convertButton = new JButton("Convert");
        convertButton.addActionListener(this);
        add(convertButton);

        resultLabel = new JLabel("Result: ");
        add(resultLabel);

        setVisible(true);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        try {
            int fromIndex = fromCurrency.getSelectedIndex();
            int toIndex = toCurrency.getSelectedIndex();
            double amount = Double.parseDouble(amountField.getText());

            if (amount < 0) {
                JOptionPane.showMessageDialog(this, "Amount must be positive", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            double result = amount * rates[fromIndex][toIndex];
            resultLabel.setText(String.format("Result: %.2f %s", result, currencyNames[toIndex]));

        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Please enter a valid number", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    public static void main(String[] args) {
        new CurrencyConverter();
    }
}

