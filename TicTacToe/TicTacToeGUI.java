import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class TicTacToeGUI extends JFrame implements ActionListener {

    private JButton[][] buttons = new JButton[3][3];
    private JButton restartButton;
    private JLabel xScoreLabel, oScoreLabel, drawLabel;

    private char currentPlayer = 'X';
    private boolean gameOver = false;

    private int xWins = 0, oWins = 0, draws = 0;

    public TicTacToeGUI() {
        setTitle("Tic Tac Toe - Java GUI with Scoreboard");
        setSize(400, 500);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // Scoreboard panel (top)
        JPanel scorePanel = new JPanel(new GridLayout(1, 3));
        xScoreLabel = new JLabel("X Wins: 0", SwingConstants.CENTER);
        oScoreLabel = new JLabel("O Wins: 0", SwingConstants.CENTER);
        drawLabel = new JLabel("Draws: 0", SwingConstants.CENTER);

        xScoreLabel.setFont(new Font("Arial", Font.BOLD, 16));
        oScoreLabel.setFont(new Font("Arial", Font.BOLD, 16));
        drawLabel.setFont(new Font("Arial", Font.BOLD, 16));

        scorePanel.add(xScoreLabel);
        scorePanel.add(oScoreLabel);
        scorePanel.add(drawLabel);

        // Game board panel (center)
        JPanel boardPanel = new JPanel(new GridLayout(3, 3));
        Font font = new Font("Arial", Font.BOLD, 60);
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                buttons[i][j] = new JButton("");
                buttons[i][j].setFont(font);
                buttons[i][j].addActionListener(this);
                boardPanel.add(buttons[i][j]);
            }
        }

        // Restart button panel (bottom)
        JPanel bottomPanel = new JPanel();
        restartButton = new JButton("Restart Game");
        restartButton.setFont(new Font("Arial", Font.BOLD, 20));
        restartButton.addActionListener(e -> resetGame());
        restartButton.setVisible(false); // 🔹 Hidden initially
        bottomPanel.add(restartButton);

        // Add panels to frame
        add(scorePanel, BorderLayout.NORTH);
        add(boardPanel, BorderLayout.CENTER);
        add(bottomPanel, BorderLayout.SOUTH);

        setVisible(true);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (gameOver) return;

        JButton clicked = (JButton) e.getSource();
        if (!clicked.getText().equals("")) return;

        clicked.setText(String.valueOf(currentPlayer));

        if (checkWin()) {
            JOptionPane.showMessageDialog(this, "Player " + currentPlayer + " wins! 🎉");
            if (currentPlayer == 'X') xWins++;
            else oWins++;
            updateScoreboard();
            gameOver = true;
            restartButton.setVisible(true); // 🔹 Show on win
        } else if (isDraw()) {
            JOptionPane.showMessageDialog(this, "It's a draw! 😐");
            draws++;
            updateScoreboard();
            gameOver = true;
            restartButton.setVisible(true); // 🔹 Show on draw
        } else {
            currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
        }
    }

    private boolean checkWin() {
        for (int i = 0; i < 3; i++) {
            if (equal(buttons[i][0], buttons[i][1], buttons[i][2])) return true;
            if (equal(buttons[0][i], buttons[1][i], buttons[2][i])) return true;
        }
        return equal(buttons[0][0], buttons[1][1], buttons[2][2]) ||
               equal(buttons[0][2], buttons[1][1], buttons[2][0]);
    }

    private boolean equal(JButton b1, JButton b2, JButton b3) {
        return !b1.getText().equals("") &&
               b1.getText().equals(b2.getText()) &&
               b2.getText().equals(b3.getText());
    }

    private boolean isDraw() {
        for (JButton[] row : buttons) {
            for (JButton btn : row) {
                if (btn.getText().equals("")) return false;
            }
        }
        return true;
    }

    private void resetGame() {
        for (JButton[] row : buttons) {
            for (JButton btn : row) {
                btn.setText("");
            }
        }
        currentPlayer = 'X';
        gameOver = false;
        restartButton.setVisible(false); // 🔹 Hide again
    }

    private void updateScoreboard() {
        xScoreLabel.setText("X Wins: " + xWins);
        oScoreLabel.setText("O Wins: " + oWins);
        drawLabel.setText("Draws: " + draws);
    }

    public static void main(String[] args) {
        new TicTacToeGUI();
    }
}


