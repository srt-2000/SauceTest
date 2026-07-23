"""Write ``OrderSummaryDTO`` to an XLSX report."""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.worksheet.worksheet import Worksheet

from services.constants import Values
from domains.order import OrderSummaryDTO


class OrderXLSXExporter:
    """Export checkout overview data into a single-sheet XLSX workbook."""

    @staticmethod
    def _apply_bold(sheet: Worksheet, cells: tuple[str, ...]) -> None:
        """Apply bold font to the given cell addresses.

        Args:
            sheet: Active openpyxl worksheet.
            cells: Cell addresses to bold (e.g. ``("A1", "B2")``).
        """
        bold = Font(bold=True)

        for address in cells:
            sheet[address].font = bold

    @staticmethod
    def export_order_summary_to_xlsx(
        order: OrderSummaryDTO,
        output_path: Path,
    ) -> Path:
        """Write order lines and totals top-to-bottom into an XLSX file.

        Creates parent directories if needed. Layout: item header, column
        headers, line rows, blank row, then payment/shipping/totals.

        Args:
            order: Order confirmation payload to serialize.
            output_path: Destination ``.xlsx`` path.

        Returns:
            The same ``output_path`` after a successful save.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        document_handler = Workbook()
        sheet = document_handler.active

        assert sheet is not None
        sheet.title = Values.SHEET_NAME
        sheet.append(["Items"])
        sheet.append(["Name", "Description", "QTY", "Price"])

        for line in order.lines:
            sheet.append([line.name, line.description, line.qty, float(line.price)])

        sheet.append([])

        summary_rows: tuple[tuple[str, object], ...] = (
            ("Payment Information", order.payment_info),
            ("Shipping Information", order.shipping_info),
            ("Ship To", order.ship_to),
            ("Item Total", float(order.items_total)),
            ("Tax", float(order.tax)),
            ("Total", float(order.total)),
        )
        # summary_start = sheet.max_row + 1

        for label, value in summary_rows:
            sheet.append([label, value])

        # self._apply_bold(
        #     sheet,
        #     (
        #         "A1",  # Items
        #         "A2",
        #         "B2",
        #         "C2",
        #         "D2",  # headers
        #         *(f"A{summary_start + i}" for i in range(len(summary_rows) + 1)),
        #     ),
        # )

        # sheet.column_dimensions["A"].width = 28
        # sheet.column_dimensions["B"].width = 55
        # sheet.column_dimensions["C"].width = 8
        # sheet.column_dimensions["D"].width = 12

        document_handler.save(output_path)
        return output_path