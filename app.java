import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class ParticleSystem extends JPanel {

    private List<Particle> particles;

    public ParticleSystem() {
        particles = new ArrayList<>();
        setPreferredSize(new Dimension(800, 600));
        setBackground(Color.BLACK);
        generateParticles(100);
    }

    private void generateParticles(int count) {
        Random random = new Random();
        for (int i = 0; i < count; i++) {
            int x = random.nextInt(getWidth());
            int y = random.nextInt(getHeight());
            int size = random.nextInt(10) + 1;
            int speedX = random.nextInt(5) - 2;
            int speedY = random.nextInt(5) - 2;
            Color color = new Color(random.nextInt(256), random.nextInt(256), random.nextInt(256));
            particles.add(new Particle(x, y, size, speedX, speedY, color));
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        for (Particle particle : particles) {
            particle.update();
            particle.draw(g);
        }
        try {
            Thread.sleep(10);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        repaint();
    }

    private static class Particle {
        private int x;
        private int y;
        private int size;
        private int speedX;
        private int speedY;
        private Color color;

        public Particle(int x, int y, int size, int speedX, int speedY, Color color) {
            this.x = x;
            this.y = y;
            this.size = size;
            this.speedX = speedX;
            this.speedY = speedY;
            this.color = color;
        }

        public void update() {
            x += speedX;
            y += speedY;
            if (x < 0 || x > 800) {
                speedX *= -1;
            }
            if (y < 0 || y > 600) {
                speedY *= -1;
            }
        }

        public void draw(Graphics g) {
            g.setColor(color);
            g.fillOval(x, y, size, size);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Particle System");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.getContentPane().add(new ParticleSystem());
            frame.pack();
            frame.setLocationRelativeTo(null);
            frame.setVisible(true);
        });
    }
}