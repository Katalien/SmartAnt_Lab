// package com.test.student;
// import java.io.FileWriter;
// import com.game.GameField;
// import com.play.Optimizer;
// import org.junit.jupiter.api.Test;
// import java.io.IOException;
// import java.time.Duration;
// import java.io.*;
//
// import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
//
// public class ResultTest {
//     public static final String ANSI_GREEN = "\u001B[32m";
//     private static final String FIELD_FILENAME = "fieldFiles/field.csv";
//     private static final int TIMEOUT_SECONDS = 50;
//
//     @Test
//     public void testResult() throws IOException {
//         GameField field = new GameField();
//         field.fill(FIELD_FILENAME);
//         assertTimeoutPreemptively(Duration.ofSeconds(TIMEOUT_SECONDS), () -> {
//                     boolean[] bestChromosome = Optimizer.optimize(field);
//                     System.out.println(ANSI_GREEN + "Your result is " + field.testAnt(bestChromosome));
//                     System.out.println(ANSI_GREEN + "Max is 89");
//                     String fileName = "result/hueta.csv";
//                     File file = new File(fileName);
//
//                     try { // Проверяем, существует ли файл
//                         if (file.exists()) {
//                             // Если файл уже есть, то перезаписываем в нем данные
//                             FileWriter writer = new FileWriter(fileName, false);
//                             String s = Integer.toString(field.testAnt(bestChromosome));
//                             writer.write(s);
//                             writer.close();
//                         } else {
//                                 // Если файла нет, то создаем новый файл
//                             file.createNewFile();
//                             FileWriter writer = new FileWriter(fileName);
//                             String s = Integer.toString(field.testAnt(bestChromosome));
//                             writer.write(s);
//                             writer.close();
//                         }
//                     } catch (IOException e) {
//                     System.out.println("Произошла ошибка: " + e.getMessage());
//                    }
//                 }
//         );
//     }
// }

package com.test.student;
import java.io.FileWriter;
import com.game.GameField;
import com.play.Optimizer;
import org.junit.jupiter.api.Test;
import java.io.IOException;
import java.time.Duration;
import java.io.*;

import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;

public class ResultTest {
    public static final String ANSI_GREEN = "\u001B[32m";
    private static final String FIELD_FILENAME = "fieldFiles/field.csv";
    private static final int TIMEOUT_SECONDS = 50;

    @Test
    public void testResult() throws IOException {
        GameField field = new GameField();
        field.fill(FIELD_FILENAME);
        assertTimeoutPreemptively(Duration.ofSeconds(TIMEOUT_SECONDS), () -> {
                    boolean[] bestChromosome = Optimizer.optimize(field);
                    System.out.println(ANSI_GREEN + "Your result is " + field.testAnt(bestChromosome));
                    System.out.println(ANSI_GREEN + "Max is 89");
                    String fileName = "result/hueta.csv";
                    File file = new File(fileName);

                    try { // Проверяем, существует ли файл
                        if (file.exists()) {
                            // Если файл уже есть, то перезаписываем в нем данные
                            FileWriter writer = new FileWriter(fileName, false);
                            String s = Integer.toString(field.testAnt(bestChromosome));
                            writer.write(s);
                            writer.close();
                        } else {
                                // Если файла нет, то создаем новый файл
                            file.createNewFile();
                            FileWriter writer = new FileWriter(fileName);
                            String s = Integer.toString(field.testAnt(bestChromosome));
                            writer.write(s);
                            writer.close();
                        }
                    } catch (IOException e) {
                    System.out.println("Произошла ошибка: " + e.getMessage());
                   }
                }
        );
    }
}